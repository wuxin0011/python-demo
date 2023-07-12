/*
 * @Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 * @Date: 2023-06-15 09:48:28
 * @LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 * @LastEditTime: 2023-06-30 10:36:15
 * @FilePath: \geruili\static\js\pagenationJs.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
var bannersw = new Swiper('.bannersw', {
	autoplay: true, //可选选项，自动滑动
	loop: true,
	effect: 'fade',
	speed: 300,
	autoplay: {
		delay: 3000
	},
	pagination: {
		el: '.bannerpage',
		type: 'bullets',
		//type: 'fraction',
		//type : 'progressbar',
		//type : 'custom',
		clickable: true,
	},
	navigation: {
		nextEl: '.swiper-button-next',
		prevEl: '.swiper-button-prev',
	},
});
var mySwiper = new Swiper('.example-swiper', {
	grabCursor: true,
	centeredSlides: true,
	slidesPerView: '3',
	spaceBetween : 20,
	loop: true,
	pagination: {
		el: '.swiper-pagination',
		clickable: true,
	},
	navigation: {
	     nextEl: '.swiper-button-next',
	     prevEl: '.swiper-button-prev',
	   },
	on: {
		slideChange: function() {
			$(".example-swiper-pagination-item").each((index, elem) => {
				if (index == this.realIndex) {
			 	$(elem).addClass("example-swiper-pagination-item-active");
				} else {
					$(elem).removeClass("example-swiper-pagination-item-active");
				}
			});

		}
	},
	breakpoints: {
		0: {
			slidesPerView: 1,
		},
		640: {
			slidesPerView: 1,
		},
		800:{
			slidesPerView:3,
		},
		900: {
			slidesPerView: 3,
		},
        1100:{
			slidesPerView: 3,
		},
		1200:{
			slidesPerView: 3,
		},
		1300: {
			slidesPerView: 3,
		},
		1500: {
			slidesPerView:3,
		},
	},
});
