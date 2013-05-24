var SkillBankView = Backbone.View.extend({
	el: $('#contentTopId'),
	tagName: 'p'	,
	initialize : function(){
		this.render();
	},
	render: function(){
		var template = _.template( $("#search_template").html(), {username: this.model.attributes.name});
		this.$el.append(template);
		return this;
	}
});
