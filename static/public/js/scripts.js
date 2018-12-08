$('body').show();
$('.version').text(NProgress.version);
NProgress.start();
setTimeout(function() {
	NProgress.done();
	$('.fade').removeClass('out')
}, 1000);

function setCookie(name, value, time) {
	var strsec = getsec(time);
	var exp = new Date();
	exp.setTime(exp.getTime() + strsec * 1);
	document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString()
}
function getsec(str) {
	var str1 = str.substring(1, str.length) * 1;
	var str2 = str.substring(0, 1);
	if (str2 == "s") {
		return str1 * 1000
	} else if (str2 == "h") {
		return str1 * 60 * 60 * 1000
	} else if (str2 == "d") {
		return str1 * 24 * 60 * 60 * 1000
	}
}
function getCookie(name) {
	var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
	if (arr = document.cookie.match(reg)) {
		return unescape(arr[2])
	} else {
		return null
	}
}
$.fn.navSmartFloat = function() {
	var position = function(element) {
			var top = element.position().top,
				pos = element.css("position");
			$(window).scroll(function() {
				var scrolls = $(this).scrollTop();
				if (scrolls > top) {
					$('.header-topbar').fadeOut(0);
					if (window.XMLHttpRequest) {
						element.css({
							position: "fixed",
							top: 0
						}).addClass("shadow")
					} else {
						element.css({
							top: scrolls
						})
					}
				} else {
					$('.header-topbar').fadeIn(500);
					element.css({
						position: pos,
						top: top
					}).removeClass("shadow")
				}
			})
		};
	return $(this).each(function() {
		position($(this))
	})
};
$("#navbar").navSmartFloat();
$("#gotop").hide();
$(window).scroll(function() {
	if ($(window).scrollTop() > 100) {
		$("#gotop").fadeIn()
	} else {
		$("#gotop").fadeOut()
	}
});
$("#gotop").click(function() {
	$('html,body').animate({
		'scrollTop': 0
	}, 500)
});
$("img.thumb").lazyload({
	placeholder: "../images/occupying.png",
	effect: "fadeIn"
});
$(".single .content img").lazyload({
	placeholder: "../images/occupying.png",
	effect: "fadeIn"
});
$('[data-toggle="tooltip"]').tooltip();
$(window).scroll(function() {
	var sidebar = $('.sidebar');
	var sidebarHeight = sidebar.height();
	var windowScrollTop = $(window).scrollTop();
	if (windowScrollTop > sidebarHeight - 60 && sidebar.length) {
		$('.fixed').css({
			'position': 'fixed',
			'top': '70px',
			'width': '360px'
		})
	} else {
		$('.fixed').removeAttr("style")
	}
});
(function() {
	var oMenu = document.getElementById("rightClickMenu");
	document.oncontextmenu = function(event) {
		$(oMenu).fadeOut(0);
		var event = event || window.event;
		var style = oMenu.style;
		$(oMenu).fadeIn(300);
		style.top = event.clientY + "px";
		style.left = event.clientX + "px";
		return false
	};
	document.onclick = function() {
		$(oMenu).fadeOut(100);
	}
})();
