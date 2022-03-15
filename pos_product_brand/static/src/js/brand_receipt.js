odoo.define('module_name.receipt', function(require){
    "use strict";
    var models = require('point_of_sale.models');
    models.load_fields('product.product', 'brand_id');
    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        export_for_printing: function(){
            var line = _super_orderline.export_for_printing.apply(this, arguments);
            line.brand_id = this.get_product().brand_id;
            return line;
        }
    });
});