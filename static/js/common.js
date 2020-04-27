$(document).ready(function(){

	//menu mob
	$('.header-bar, .header-close').on('click', function(){
		$('.header').toggleClass('header-open');
		$('.header-search').removeClass('search-open');
	});

	$('.header-quest,.search-close').on('click', function(){
		$('.header-search').toggleClass('search-open');
		$('.header').removeClass('header-open');
	});

	$('.drop.drop-second .drop-arrow').on('click', function(e){
		//e.preventDefault();
		if($(window).width() <= 1020)
			$(this).next('.drop-list').slideToggle(200).parents('.drop.drop-second').toggleClass('drop-active');
	});

	$(document).on('click', function (e){
		var block = $(".header");
		if (!block.is(e.target) && block.has(e.target).length === 0)
			$('.header').removeClass('header-open');
	});

	//menu scroll
	$('.scroll-link').on('click', function(e){
		e.preventDefault();
		var itemId = $(this).attr('href'),
				blockTop = $(itemId).offset().top - 60;
		$('html, body').animate({scrollTop : blockTop},900);

		if($(window).width() <= '1020'){
			$('.header').toggleClass('header-open');
		}
	});

	//tab
	$('.tab-list li a').on('click', function(e){
		e.preventDefault();

		$('.tab-list li a').removeClass('active');
		$('.tab').removeClass('tab-active');

		var attr = $(this).attr('href');
		$(attr).addClass('tab-active');
		$(this).addClass('active');
	});

	//modal
	var modalCont = $('.modal');
		
	$('.button-modal').on('click',function(e){
		e.preventDefault();
		var id = $(this).attr('href');
		$(modalCont).removeClass('open');
		$(id).addClass('open');
		$('.modal-overlay').addClass('open-overlay');
	});

	$('.cancel, .modal-overlay').on('click',function(){
		$(modalCont).removeClass('open');
		$('.modal-overlay').removeClass('open-overlay');
	});

});