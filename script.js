// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    console.log('网页已加载完成！');
    
    // 获取所有导航链接
    const navLinks = document.querySelectorAll('nav a');
    
    // 为每个链接添加点击事件
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            // 平滑滚动到目标区域
            targetSection.scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // 修改欢迎标题
    const welcomeHeading = document.querySelector('header h1');
    welcomeHeading.textContent = '欢迎访问我的网站';
});