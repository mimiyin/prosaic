function scroll(current, wordsies, callback) {
	//console.log("SCROLLING: " + wordsies.toString());
	// Size the animation div according to longest word
	var theWordsie = '#word' + current;
	
	var countDiv = $('<div>').addClass('count').attr('id', 'count-for-' + current).text(current+1);
	var wordDiv = $('<div>').addClass('word').attr('id', current);
	$('body').append(countDiv).append(wordDiv);	
	
		
	// Figure out max font-size for this phrase
	var max = 100 * 2/wordsies.length;
	wordDiv.text(wordsies);
	wordDiv.css('font-size', 0);
	
	var width = $(window).width();
	var height = $(window).height();
	
	// Move the starting point of the animation
	wordDiv.css({
		'width'	: '100%',
		'float'	: 'left',
		//'left' : 0,
		});
	
	//console.log(wordDiv);
	
	
	/* Delay the animation some arbitrary amount
	 * Set amount of time and velocity curve for text to grow
	 * Set amount of time and velocity curve for text to shrink
	 */
	wordDiv.delay(delay).animate({
		fontSize: max + 'vw',
		}, wordsies.length*Math.pow(2, .5)*20 + 250, function(){ 
			var id = $(this).attr('id');
			$("#count-for-" + id).remove();
			callback();

			$(this)
				.animate({
					bottom: '+=' + ($(this).height()*Math.log(.5)) + 'px',
					fontSize: 0,
					opacity : 0,
				}, 5000, function(){
					$(this).remove();
				});
		});
	}

