let length = 305;
$(function() {
	
	$("a.ant").click(function(){
		
		$("a.ant").removeClass("active");
		$(this).addClass("active");
		
		let i = $(this).index();
		$("div.reLo").css("display","none");
		$("div.reLo").eq(i).css("display","block");
		 
		let hr = $("div.ss_hr");
		if( i == 1){
			hr.css({'transform':'translateX('+length+'px)'});
		}
		else{
			hr.css({'transform':'translateX('+0+'px)'});
		}
	});
	
});