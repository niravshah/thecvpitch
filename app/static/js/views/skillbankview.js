var SkillBankView = Backbone.View.extend({
	el: $('#contentTopId'),
	tagName: 'p'	,
	template: _.template($('#template1').html()),
	initialize : function(){
		this.render();
	},
	render: function(){
		this.$el.append(this.template({username: this.model.attributes.name}));
		return this;
	}
});
