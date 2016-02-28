var cycleCities = function() {
    var callRandom = function() {
	randomCity();;
    }
    
    var i = 0;
    setInterval(function(){
	callRandom();
	i++;
    }, 7000);
}


$(function() {
    cycleCities();
});
