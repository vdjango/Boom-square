var xmlHttp;

function createXMLHttpRequest() {
    if (window.ActiveXObject)
        xmlHttp = new ActiveXObject('Microsoft.XMLHTTP');
    else if (window.XMLHttpRequest)
        xmlHttp = new XMLHttpRequest();
}

//GET的发送方式  
function startRequest() {
    createXMLHttpRequest();
    xmlHttp.open('GET', '/update/back/', true); //GET发送数据的方式  
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) //判断返回码  
            return xmlHttp.responseText
        alert('已经连接' + xmlHttp.responseText)
    }
    xmlHttp.send(null); //GET发送的内容不再send(）中  
}

//POST的发送方式  
function startPOST() {
    createXMLHttpRequest();
    xmlHttp.open('POST', '/update/back/', true);
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            alert('POST已经连接' + xmlHttp.responseText)
    }
    xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded"); //<span style="color:#ff0000;">POST发送必须加请求头</span>  
    xmlHttp.send('name=littlepost');
}


var progressbar={
    init:function(){
        startRequest();
        var fill=document.getElementById('fill');
        var count=0;

    //通过间隔定时器实现百分比文字效果,通过计算CSS动画持续时间进行间隔设置
        var timer=setInterval(function(e){
            count++;
            fill.innerHTML=count+'%';
            if(count===100) clearInterval(timer);
        },17);
    }
};
progressbar.init();