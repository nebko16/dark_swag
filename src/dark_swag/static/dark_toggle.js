document.addEventListener('DOMContentLoaded',function(){
    var span=document.createElement('span');
    span.textContent=' 🌙 Dark Mode';
    span.style.textShadow='0 0 12px rgba(0, 0, 0, 1)';
    span.style.position='absolute';
    span.style.right='16px';
    span.style.top='-32px';
    span.style.color='rgba(0,0,0,1)';
    span.style.cursor='pointer';
    span.style.paddingLeft='20px';span.addEventListener('click',function(){window.location.href='/docs';});document.querySelector('.swagger-ui').appendChild(span);});