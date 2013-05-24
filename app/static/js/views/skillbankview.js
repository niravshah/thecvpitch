var SkillBankView = Backbone.View.extend({
	el: $('#contentTopId'),
	tagName: 'p'	,
	initialize : function(){
		this.render();
	},
	render: function(){
		tmp = $.get('/static/js/templates/template1.htm');
		var template = _.template( tmp.responseText, {username: this.model.attributes.name});
		this.$el.append(template);
		return this;
	}
});
