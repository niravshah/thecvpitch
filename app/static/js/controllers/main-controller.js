var MainController = Backbone.Router.extend({
	routes:{
		"skillbank/:username" : "skillbank"
	}

});

var maincont = new MainController();

maincont.on('route:skillbank', function(username){
                var sbank = new skillbank({id:username});
                sbank.fetch({
                        success : function(){
				skillBankRegion.show( new skillBankView({model:sbank}));
			},
                        error : function(){
                                new Error({message: "Error loading the Skill Bank for User"});
                        }
                });
	});
