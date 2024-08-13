function addDarkModeToggle() {
    let span=document.createElement('span');
    span.textContent=" ☀️ Light Mode";
    span.style.position='absolute';
    span.style.right = '14px';
    span.style.top = '6px';
    span.style.color='rgba(255, 255, 255, 1)';
    span.style.cursor='pointer';
    span.style.paddingLeft='20px';
    span.addEventListener('click',function(){
        window.location.href='/docs_light';
    });

    let observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                let swaggerBody = document.getElementById('swagger-ui');
                if (swaggerBody) {
                    swaggerBody.appendChild(span);
                    observer.disconnect();
                }
            }
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
}

document.addEventListener('DOMContentLoaded', addDarkModeToggle);
