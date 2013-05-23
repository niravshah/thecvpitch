(function($){
var ListView = Backbone.View.extend({
el: $('.nav'), 
events: {
	'click a#lidashboard': 'addItem'
},
initialize: function(){
	alert('init');
},
render: function(){
},
addItem: function(){
	alert ('addItem');
}
});
var listView = new ListView();
})(jQuery); 
