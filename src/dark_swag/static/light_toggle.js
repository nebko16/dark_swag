document.addEventListener('DOMContentLoaded',function(){
    var span=document.createElement('span');
    span.textContent=" ☀️ Light Mode";
    span.style.position='absolute';
    span.style.right='16px';
    span.style.top='-32px';
    span.style.color='#ffffff';
    span.style.cursor='pointer';
    span.style.paddingLeft='20px';
    span.addEventListener('click',function(){
        window.location.href='/docs_light';
    });
    document.querySelector('.swagger-ui').appendChild(span);
});