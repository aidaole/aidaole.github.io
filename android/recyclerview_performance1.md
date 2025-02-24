# 关于RecyclerView的一些优化方法

RecyclerView 是 Android 中一个非常重要的控件，它可以帮助我们实现列表、网格等多种布局效果。然而，在使用 RecyclerView 时，我们也需要注意一些性能优化的问题，以提高应用的流畅度和响应速度。

以下是一些关于 RecyclerView 的性能优化方法：

# 理解 RecyclerView 的工作原理

RecyclerView 可以理解成一个没有边界的列表, 里面存放了很多的itemview. 比如我们有1000个item的数据, 都通过apdater填充给recyclerview, 但是一次全部加载出来, 渲染就会相当慢. 所以我们需要做的就是按需加载, 只加载当前屏幕可见的item. 单滑动的时候, 通过同类型itemview复用的方式, 将新item的数据通过 onBindViewHolder 绑定到缓存的 itemview上, 即可显示出来. 

那么recyclerview的缓存机制是怎么样的呢?

当 RecyclerView 需要显示一个 Item（调用 getViewForPosition）时，会按照以下顺序尝试获取 ViewHolder：

## 第一层：Scrap（临时缓存）
定义：存储当前屏幕上或即将离开屏幕的 ViewHolder，这些 ViewHolder 仍然与数据绑定状态保持一致。
特点：不按类型（viewType）分类，仅按位置（position）管理。
分为两种：
* Attached Scrap：屏幕上可见的 ViewHolder（已绑定到 RecyclerView）。
* Detached Scrap：因滑动或布局变化暂时脱离屏幕但还未回收的 ViewHolder。
存储位置：mAttachedScrap（ArrayList）和 mChangedScrap（ArrayList）。
生命周期：仅在一次布局计算（layout pass）中有效，之后会被回收或销毁。

## 第二层：Cache（缓存视图）
定义：存储最近离开屏幕的 ViewHolder，仍然保留绑定数据，但可能需要重新绑定（rebind）。
特点：数量有限，默认缓存大小由 mViewCacheMax 控制（默认值为2，可通过 setItemViewCacheSize 修改）。按位置管理，不按类型分类。
存储位置：mCachedViews（ArrayList）。
作用：快速复用刚滑出屏幕的 ViewHolder，避免频繁创建或从池中获取。

## 第三层：ViewCacheExtension（自定义缓存）
定义：开发者通过 RecyclerView.ViewCacheExtension 提供的扩展缓存，完全自定义。
特点：默认不启用（null），需手动实现。不受 RecyclerView 内部限制，可按位置或类型缓存完整的 View。
存储位置：由开发者定义（如 Map 或 List）。
作用：适用于特殊场景（如预加载或跨区域复用）。

## 第四层：RecycledViewPool（回收池）
定义：存储已销毁但可按类型复用的 ViewHolder，是最终的缓存池。
特点：按 viewType 分类管理，每个类型默认缓存5个 ViewHolder（可通过 setMaxRecycledViews 修改）。不保留数据绑定状态，仅保留 View 的结构。
存储位置：mRecyclerPool（RecyclerView.RecycledViewPool）。
作用：长期缓存 ViewHolder，供不同 RecyclerView 或同一 RecyclerView 的不同区域复用。

## 最后新建 ViewHolder：
如果以上都未命中，调用 onCreateViewHolder 创建新 ViewHolder，然后绑定数据。
场景：首次加载或缓存耗尽。

利用这些缓存空间, 我们可以做一些优化, 比如说: 内存, 加载速度, viewbind

# 优化手段

## 1. 设置划出屏幕缓存个数

当列表快速滑动的时候, 划出屏幕的itemview会被缓存, 当再次滑动回来的时候, 会从缓存中取出, 而不是重新创建, 这样可以提高滑动的流畅度. 默认为2, 如果想提高服用概率避免重复创建, 可以将cachesize设置大一点. 这种主要是针对划出屏幕就被回收的场景.

```kotlin
recyclerView.setItemViewCacheSize(10)
```

## 2. 根据viewtype缓存个数

比如列表是4中类型, 那么可以在缓存中设置不同的缓存个数, 这样可以提高复用的概率. 也可以避免快速滑动的时候一直重复创建, 控制内存抖动

而且这个 shraedPoll 是可以共享的, 比如我有多个recyclerview, 里面的item类型都差不多, 那么我可以跨 recyclerview 来共享这个缓存池.

```kotlin
val sharedPoll = RecyclerView.RecycledViewPool().apply {
    setMaxRecycledViews(ItemAdapter.VIEW_TYPE_LOADING, 1)
    setMaxRecycledViews(ItemAdapter.VIEW_TYPE_TEXT, 20)
    setMaxRecycledViews(ItemAdapter.VIEW_TYPE_ITEM, 20)
    setMaxRecycledViews(ItemAdapter.VIEW_TYPE_BIGPIC, 20)
}
binding.recyclerView.setRecycledViewPool(sharedPoll)
```

## 3. 子线程预加载视图 + ViewCacheExtension, 提前加载耗时的view

比如说一些视频控件, 走 onCreateViewHolder 会和耗时, 那我是不是可以提前创建出来塞到缓存中. 当要显示这种空间时直接走onBindViewHolder 就可以了.

```kotlin
class MyViewCacheExtension(private val cacheSize: Int) : RecyclerView.ViewCacheExtension() {
    private val viewCache = mutableMapOf<Int, View>()
    private val lock = Any() // 线程同步锁

    override fun getViewForPositionAndType(
        recycler: RecyclerView.Recycler,
        position: Int,
        type: Int
    ): View? {
        synchronized(lock) {
            return viewCache[position]?.also { viewCache.remove(position) }
        }
    }

    // 在子线程中预加载视图
    fun preloadViews(context: Context, layoutId: Int, positions: List<Int>) {
        CoroutineScope(Dispatchers.Default).launch {
            val inflater = LayoutInflater.from(context.applicationContext)
            positions.forEach { position ->
                val view = inflater.inflate(layoutId, null, false) // 子线程inflate
                synchronized(lock) {
                    if (viewCache.size < cacheSize) {
                        viewCache[position] = view
                    }
                }
            }
        }
    }
}

// 在Fragment中使用
class TabFragment : Fragment() {
    private val cacheExtension = MyViewCacheExtension(5)

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        val recyclerView = view.findViewById<RecyclerView>(R.id.recycler_view)
        recyclerView.setViewCacheExtension(cacheExtension)

        // 启动预加载（不阻塞主线程）
        cacheExtension.preloadViews(requireContext(), R.layout.item_layout, (0..4).toList())
    }
}
```

# 4. 使用 DiffUitl 计算差异再 submitList, 不要使用 notifyDatasetChange

**notifyDatasetChange** 是一个老生常谈的问题, 就是调用的时候整个 recyclerview 都会刷新, 列表很大的时候就非常耗时.

所以官方推荐使用 DiffUtil 计算出新数据和老数据的差异之后, 再调用 submitList 来更新列表, 做到部分刷新.

```kotlin
class ItemDiffCallback : DiffUtil.ItemCallback<ItemData>() {
    override fun areItemsTheSame(oldItem: ItemData, newItem: ItemData): Boolean {
        // 类型一样, 比较对象id.  如果id一样再比比较所有属性
        // 所以这里的流程是 areItemsTheSame=true 的时候才会调用 areContentsTheSame
        return when {
            oldItem is ItemData.PicItem && newItem is ItemData.PicItem ->
                oldItem.id == newItem.id

            oldItem is ItemData.BigPicItem && newItem is ItemData.BigPicItem ->
                oldItem.id == newItem.id

            oldItem is ItemData.TextItem && newItem is ItemData.TextItem ->
                oldItem.id == newItem.id

            oldItem is ItemData.LoadingItem && newItem is ItemData.LoadingItem -> true
            else -> false
        }
    }

    override fun areContentsTheSame(oldItem: ItemData, newItem: ItemData): Boolean {
        return oldItem == newItem // 这里是利用kotlin的data class的equals方法来比较所有属性, 不是比较的对象引用
    }
}
```

# 5. 使用 setHasFixedSize=true, 避免重复 onMesaure

如果所有item类型的大小都不会因为内容的变化而大小变化, 就可以使用这个属性, 避免重复的 onMesure 就按

```kotlin
recyclerView.setHasFixedSize(true)
```

# 6. 提前 loadMore

做feed流的应用很常见, 就是滑动一直加载新内容. 为了让用户无感, 可以很提前就 loadMore, 这样用户时候的时候不会出现laoding, 效果更佳

```kotlin
recyclerView.addOnScrollListener(object : RecyclerView.OnScrollListener() {
    override fun onScrolled(recyclerView: RecyclerView, dx: Int, dy: Int) {
        super.onScrolled(recyclerView, dx, dy)
        val layoutManager = recyclerView.layoutManager as? StaggeredGridLayoutManager
        if (layoutManager != null && !isLoading && dy > 0) { // 没有在加载中, 并且是向下滑动
            val lastVisibleItemPositions = layoutManager.findLastVisibleItemPositions(null)
            val lastVisibleItemPosition = lastVisibleItemPositions.maxOrNull() ?: 0
            val totalItemCount = layoutManager.itemCount
            if (lastVisibleItemPosition >= totalItemCount - 10) { //提前10就开始加载新数据
                loadMoreData()
            }
        }
    }
})
private fun initViewModels() {
    viewModel.getItemsForPosition(position).observe(viewLifecycleOwner) { items ->
        adapter.removeLoadingItem() // 删除加载更多view
        adapter.appendItems(items)
        isLoading = false // 重置状态
    }
}

private fun loadMoreData() {
    if (!isLoading) {
        isLoading = true // 加载中状态, 避免重复
        adapter.addLoadingItem()
        viewModel.fetchData(position, currentPage++, pageSize)
    }
}
```

## 7. 滑动时不加载图片

这也是一个常见的优化, 就是itemview中有图片的时候, 如果快速滑动图片可能很快就被划出屏幕了, 用户根本看不到, 这种图片就可以不加载, 而是只加载当前屏幕中显示的item的图片.

很幸运的是, 如果你使用的图片库是 `coil`, 那么它是自带这个功能的

如果使用的是`Glide` 就需要手动调用, 在合适的时机调用 `pauseRequests()` 方法来暂停图片加载，然后在适当的时候调用 `resumeRequests()` 方法来恢复加载。