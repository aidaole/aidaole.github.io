# Aidaole's Blog

## 学习并记录自己的一些知识，总结和感想

> 欢迎学习交流和指正

<div class="card-container">
  <a href="/android/aimusic.md" class="card">
    <img src="images/ic_aidaole.jpeg" class="card-icon" alt="Github">
    <div class="card-title">开始阅读</div>
  </a>
  <a href="/algorithm/README.md" class="card">
    <img src="images/ic_leetcode.png" class="card-icon" alt="算法">
    <div class="card-title">算法刷起来</div>
  </a>
  <a href="https://github.com/aidaole/AiMusic" class="card">
    <div class="badge opensource">开源</div>
    <img src="images/ic_aimusic.jpg" class="card-icon" alt="开始阅读">
    <div class="card-title">AiMusic应用</div>
  </a>
  <a href="https://github.com/aidaole/EasyLaunch" class="card">
    <div class="badge opensource">开源</div>
    <img src="images/ic_easylaucn.png" class="card-icon" alt="Android">
    <div class="card-title">EasyLaunch框架</div>
  </a>
</div>

<!-- 自定义样式 -->
<style>
  .card-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 25px;
    margin: 40px 0;
  }
  
  .card {
    position: relative;
    width: 220px;
    height: 200px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 16px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    color: #333;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    border: 1px solid rgba(0, 0, 0, 0.05);
    padding: 20px;
    backdrop-filter: blur(5px);
    overflow: hidden;
  }
  
  .card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
    border-color: var(--theme-color, #42b983);
  }

  .card:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(225deg, transparent 60%, rgba(66, 185, 131, 0.1));
    z-index: -1;
    opacity: 0;
    transition: opacity 0.4s ease;
  }

  .card:hover:before {
    opacity: 1;
  }
  
  .card-icon {
    max-width: 90px;
    max-height: 90px;
    margin-bottom: 20px;
    object-fit: contain;
    filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
    transition: transform 0.3s ease;
  }

  .card:hover .card-icon {
    transform: scale(1.1);
  }
  
  .card-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--theme-color, #42b983);
    text-align: center;
    margin-top: 5px;
    position: relative;
    padding-bottom: 8px;
  }

  .card-title:after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 2px;
    background-color: var(--theme-color, #42b983);
    transition: width 0.3s ease;
  }

  .card:hover .card-title:after {
    width: 70%;
  }

  .badge {
    position: absolute;
    top: 0;
    left: 0;
    padding: 5px 10px;
    font-size: 12px;
    font-weight: bold;
    color: white;
    border-top-left-radius: 16px;
    border-bottom-right-radius: 10px;
    z-index: 2;
  }

  .badge.opensource {
    background-color: #28a745;
  }

  section.cover .cover-main h1 {
    color: var(--theme-color, #42b983);
    font-size: 4rem;
    margin: 1rem 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  section.cover .cover-main h2 {
    font-size: 1.5rem;
    margin: 1rem 0;
    color: #444;
  }

  section.cover .cover-main blockquote {
    font-size: 1.2rem;
    color: #666;
    margin: 2rem 0;
    border-left: 4px solid var(--theme-color, #42b983);
    padding-left: 20px;
  }

  @media (max-width: 768px) {
    .card-container {
      gap: 15px;
    }
    
    .card {
      width: 160px;
      height: 180px;
      padding: 15px;
    }
    
    .card-icon {
      max-width: 70px;
      max-height: 70px;
    }
    
    .card-title {
      font-size: 16px;
    }
  }
</style>

<!-- ![](images/_coverpage/2025-03-11-22-02-44.png ':size=300') -->
