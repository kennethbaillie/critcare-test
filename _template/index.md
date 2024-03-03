---
layout: home
---

<style>

body {
	background-attachment: fixed;
	color: #333;
	background: rgba(10, 10, 10, 0.8);
}

.box {
	border-radius: 3px;
	background: rgba(101, 101, 101, 0.7); margin: auto; padding: 12px;
}

.lightbox {
	zoom: 1.5;
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	text-align: center;
	margin: auto;
}

div.horizontal {
	display: flex;
	justify-content: center;
	height: 100%;
}

div.vertical {
	display: flex;
	flex-direction: column;
	justify-content: center;
	width: 100%;
}

input{
	text-align: center;
}

::-webkit-input-placeholder {
   color: #955;
   text-align: center;
}

::-moz-placeholder {
   color: #955;
   text-align: center;
}

:-ms-input-placeholder {
   color: #955;
   text-align: center;
}

</style>

<div class="col-xs-12 col-md-6 col-lg-4"></div>
<div class="col-xs-6 col-md-6 col-lg-4">
<div class="horizontal vertical">
<input id="username" type="text" placeholder="username" /> <br />
<input id="password" type="password" placeholder="password" /> <br />
<button id="loginbutton" type="button">Access</button>
<p id="wrongPassword" style="display: none">wrong password</p>
</div>
</div>
<div class="col-xs-12 col-md-6 col-lg-4"></div>

<script type="text/javascript" src="https://code.jquery.com/jquery-1.12.0.min.js"></script>

<script type="text/javascript">
	'use strict';class Sha1{static hash(msg,options){const defaults={msgFormat:'string',outFormat:'hex'};const opt=Object.assign(defaults,options);switch(opt.msgFormat){default:case 'string':msg=utf8Encode(msg);break;case 'hex-bytes':msg=hexBytesToString(msg);break;}
const K=[0x5a827999,0x6ed9eba1,0x8f1bbcdc,0xca62c1d6];const H=[0x67452301,0xefcdab89,0x98badcfe,0x10325476,0xc3d2e1f0];msg+=String.fromCharCode(0x80);const l=msg.length/4+2;const N=Math.ceil(l/16);const M=new Array(N);for(let i=0;i<N;i++){M[i]=new Array(16);for(let j=0;j<16;j++){M[i][j]=(msg.charCodeAt(i*64+j*4+0)<<24)|(msg.charCodeAt(i*64+j*4+1)<<16)|(msg.charCodeAt(i*64+j*4+2)<<8)|(msg.charCodeAt(i*64+j*4+3)<<0);}}
M[N-1][14]=((msg.length-1)*8)/Math.pow(2,32);M[N-1][14]=Math.floor(M[N-1][14]);M[N-1][15]=((msg.length-1)*8)&0xffffffff;for(let i=0;i<N;i++){const W=new Array(80);for(let t=0;t<16;t++)W[t]=M[i][t];for(let t=16;t<80;t++)W[t]=Sha1.ROTL(W[t-3]^W[t-8]^W[t-14]^W[t-16],1);let a=H[0],b=H[1],c=H[2],d=H[3],e=H[4];for(let t=0;t<80;t++){const s=Math.floor(t/20);const T=(Sha1.ROTL(a,5)+Sha1.f(s,b,c,d)+e+K[s]+W[t])>>>0;e=d;d=c;c=Sha1.ROTL(b,30)>>>0;b=a;a=T;}
H[0]=(H[0]+a)>>>0;H[1]=(H[1]+b)>>>0;H[2]=(H[2]+c)>>>0;H[3]=(H[3]+d)>>>0;H[4]=(H[4]+e)>>>0;}
for(let h=0;h<H.length;h++)H[h]=('00000000'+H[h].toString(16)).slice(-8);const separator=opt.outFormat=='hex-w'?' ':'';return H.join(separator);function utf8Encode(str){try{return new TextEncoder().encode(str,'utf-8').reduce((prev,curr)=>prev+String.fromCharCode(curr),'');}catch(e){return unescape(encodeURIComponent(str));}}
function hexBytesToString(hexStr){const str=hexStr.replace(' ','');return str==''?'':str.match(/.{2}/g).map(byte=>String.fromCharCode(parseInt(byte,16))).join('');}}
static f(s,x,y,z){switch(s){case 0:return(x&y)^(~x&z);case 1:return x^y^z;case 2:return(x&y)^(x&z)^(y&z);case 3:return x^y^z;}}
static ROTL(x,n){return(x<<n)|(x>>>(32-n));}}
if(typeof module!='undefined'&&module.exports)module.exports=Sha1;

try {
 console //does the console exist?
}
catch(e) { //if not...
 console = {}; //create a console object for IE
 console.log = function() {}; //add a log method to the new console object
 //add other console methods here if you need them
}

function loadPage(pwd) {
	var hash= pwd;
	hash= Sha1.hash(pwd);
	var url= hash + "/";
	$.ajax({
		url : url,
		dataType : "html",
		success : function(data) {
			console.log(url)
			location.protocol = "https:"
			window.location= url;
		},
		error : function(xhr, ajaxOptions, thrownError) {
						parent.location.hash= hash;
			//$("#wrongPassword").show();
			$("#password").attr("placeholder","wrong username/password");
			$("#password").val("");
		}
	});
}

function submit() {
	var target = $.trim($("#username").val()).toLowerCase()+$.trim($("#password").val()).toLowerCase()
	console.log(target);
	loadPage(target);
}

$("#loginbutton").on("click", function() {
	submit();
});
$("#password").keypress(function(e) {
	if (e.which == 13) {
		submit();
	}
});
//$("#username").focus();

</script>












