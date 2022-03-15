odoo.define('product_brand.product_brand_id_order_line', function (require) {
    "use strict";
    console.log("good")

    var models = require('point_of_sale.models');
    var _super_orderline = models.Orderline.prototype;
    models.load_fields('product.product', 'brand_id');
    models.Orderline = models.Orderline.extend({
        initialize: function(attr,options) {
            var line = _super_orderline.initialize.apply(this,arguments);
            this.brand_id = this.product.brand_id;
        },
    });
});
