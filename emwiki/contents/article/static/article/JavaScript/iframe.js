// for saving in rs
var mizhtm='';
function hs(obj)
{
// document.getElementById('myimage').nextSibling.style.display = 'block';
if (obj.nextSibling.style.display == 'inline')
 { obj.nextSibling.style.display = 'none'; }
else { if (obj.nextSibling.style.display == 'none')
 { obj.nextSibling.style.display = 'inline'; }
 else { obj.nextSibling.style.display = 'inline';  }}
return false;
}

function hs2(obj)
{
if (obj.nextSibling.style.display == 'block')
 { obj.nextSibling.style.display = 'none'; }
else { if (obj.nextSibling.style.display == 'none')
 { obj.nextSibling.style.display = 'block'; }
 else { obj.nextSibling.style.display = 'none';  }}
return false;
}
function hsNdiv(obj)
{
var ndiv = obj;
while (ndiv.nextSibling.nodeName != 'DIV') { ndiv = ndiv.nextSibling; }
return hs2(ndiv);
}

// remote request cache - for each url its http_request.responseText
var rrCache= {};
rrCache[0]='';

// explorer7 implements XMLHttpRequest in some strange way
// optional tooltip is passed to insertRequest
function makeRequest(obj,url,tooltip) 
{
    // if the result is cached, insert it now
    if (rrCache[url] != null)
    {
	insertRequest(obj,null,url,tooltip);
    }
    else
    {
        var http_request = false;
        if (window.XMLHttpRequest && !(window.ActiveXObject)) { // Mozilla, Safari,...
            http_request = new XMLHttpRequest();
            if (http_request.overrideMimeType) {
                http_request.overrideMimeType('text/xml');
            }
        } else if (window.ActiveXObject) { // IE
            try {
                http_request = new ActiveXObject('Msxml2.XMLHTTP');
            } catch (e) {
                try {
                    http_request = new ActiveXObject('Microsoft.XMLHTTP');
                } catch (e) {}
            }
        }
        if (!http_request) {
            alert('Giving up :( Cannot create an XMLHTTP instance');
            return false;
        }
        http_request.onreadystatechange = function() { insertRequest(obj,http_request,url,tooltip); };
        http_request.open('GET', url, true);
        http_request.send(null);
    }
}
// commented the 200 state to have local requests too
// if tooltip nonnil, obj.innerHTML is changed, and the result is put in rrCache
function insertRequest(obj,http_request,url,tooltip) 
{
    var respText = null;
    if(http_request == null) // no request done, we are called with cached result
    {
	respText = rrCache[url];
    }
    else { if (http_request.readyState == 4) { 
	respText = http_request.responseText; 
    }}

    if (respText != null) 
    {
//            if (http_request.status == 200) {
	if(http_request != null) {rrCache[url] = respText;}
	if(tooltip != null)
	{
	    obj.innerHTML = respText;	    
	}
	else
	{
	    var ndiv = obj;
	    while (ndiv.nodeName != 'SPAN') { ndiv = ndiv.nextSibling; }
	    ndiv.innerHTML = respText;
	    obj.onclick = function(){ return hs2(obj) };
	}
    }
}

// simple tooltips
var tooltip=function(){
 var id = 'tt';
 var top = 3;
 var left = 3;
 var maxw = 500;
 var speed = 10;
 var timer = 2;
 var endalpha = 95;
 var alpha = 0;
 var tt,t,c,b,h;
 var ie = document.all ? true : false;
 return{
  show:function(how,v,w){
   if(tt == null){
    tt = document.createElement('div');
    tt.setAttribute('id',id);
    document.body.appendChild(tt);
    tt.style.opacity = 0;
    tt.style.filter = 'alpha(opacity=0)';
    document.onmousemove = this.pos;
   }

   tt.style.display = 'block';
   if(how == 'url')
   {
       if(rrCache[v]==null) { 
	   tt.innerHTML ='<div>loading...</div>'; 
	   makeRequest(tt,v,1); 
       } else { 
	   tt.innerHTML = rrCache[v]; 
       }
   }
   else { if ((how == 'hs') || (how == 'hs2')) { tt.innerHTML = v.nextSibling.innerHTML; }
   else { if (how == 'txt') { tt.innerHTML = v; }
	  else { tt.innerHTML = ''; }
	}
   }

   tt.style.width = w ? w + 'px' : 'auto';
   if(!w && ie){
    tt.style.width = tt.offsetWidth;
   }
  if(tt.offsetWidth > maxw){tt.style.width = maxw + 'px'}
  h = parseInt(tt.offsetHeight) + top;
  clearInterval(tt.timer);
  tt.timer = setInterval(function(){tooltip.fade(1)},timer);
  },
  pos:function(e){
   var u = ie ? event.clientY + document.documentElement.scrollTop : e.pageY;
   var l = ie ? event.clientX + document.documentElement.scrollLeft : e.pageX;
   tt.style.top = (u - h) + 'px';
   tt.style.left = (l + left) + 'px';
  },
  fade:function(d){
   var a = alpha;
   if((a != endalpha && d == 1) || (a != 0 && d == -1)){
    var i = speed;
   if(endalpha - a < speed && d == 1){
    i = endalpha - a;
   }else if(alpha < speed && d == -1){
     i = a;
   }
   alpha = a + (i * d);
   tt.style.opacity = alpha * .01;
   tt.style.filter = 'alpha(opacity=' + alpha + ')';
  }else{
    clearInterval(tt.timer);
     if(d == -1){tt.style.display = 'none'}
  }
 },
 hide:function(){tt.style.display  = 'none';}
 };
}();

// reference show/hide - shortened because frequent, just a wrapper to tooltip.show/hide
function rs(ref) { tooltip.show('url', mizhtm + 'refs/' + ref); }
function rh() { tooltip.hide(); } 


MathJax.Hub.Config({                                                                                                                            
    extensions: ['tex2jax.js'],                                                                                                                   
    jax: ['input/TeX', 'output/HTML-CSS'],                                                                                                        
    tex2jax: {                                                                                                                                    
        inlineMath: [ ['$','$'], ['\(','\)'] ],                                                                                                   
        displayMath: [ ['$$','$$'], ['\[','\]'] ],                                                                                                
        processClass: 'mathjax',                                                                                                                        
        ignoreClass: 'no-mathjax',                                                                                                                      
        processEscapes: true,                                                                                                                       
    },                                                                                                                                            
    'HTML-CSS': {   scale: 80, availableFonts: ['TeX'] }                                                                                     
  });