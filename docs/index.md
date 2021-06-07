<style>

body {

	background-attachment: fixed;
	color: #333;
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
	background: rgba(10, 10, 10, 0.8);
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

<div id="loginbox" class="lightbox" >
	<div class="horizontal">
		<div class="vertical">
			<div class="box">
				<input style="margin: 16px; text-align: center;" id="username" type="text" placeholder="username" /> <br />
				<input style="margin: 16px; text-align: center;" id="password" type="password" placeholder="password" /> <br />
				<button id="loginbutton" type="button">Access</button>
				<p id="wrongPassword" style="display: none">wrong password</p>
			</div>
		</div>
	</div>
</div>

<script type="text/javascript" src="https://code.jquery.com/jquery-1.12.0.min.js"></script>
<script type="text/javascript" src="js/sha1.js"></script>
<script type="text/javascript">
"use strict";

//code to catch error in IE because it doesn't have a console
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
	var url= hash + "/index.html";

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
			$("#password").attr("placeholder","wrong password");
			$("#password").val("");
		}
	});
}

$("#loginbutton").on("click", function() {
	loadPage($("#username").val()+$("#password").val());
});
$("#password").keypress(function(e) {
	if (e.which == 13) {
		//loadPage($("#password").val());
		loadPage($.trim($("#username").val())+$.trim($("#password").val()));
	}
});
//$("#username").focus();

</script>












