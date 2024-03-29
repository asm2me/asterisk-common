  odoo.define("asterisk_base.tree_buttons", function (require) {
  "use strict";

  var session = require('web.session');
  var ListController = require('web.ListController');
  var FormController = require('web.FormController');  
  
  var AstBaseListController = ListController.include({
    
    renderButtons: function($node) {
        this._super.apply(this, arguments)
        if (this.$buttons) {
          let apply_btn = this.$buttons.find('.o_apply_changes');
          apply_btn && apply_btn.click(this.proxy('asterisk_base_apply_changes'));
          let bans_btn = this.$buttons.find('.o_reload_access_bans');
          bans_btn && bans_btn.click(this.proxy('asterisk_base_reload_access_bans'));
        }
    },

    asterisk_base_apply_changes: function () {
      this._rpc({
        model: 'asterisk_base.server',
        method: 'apply_all_changes',
        kwargs: {notify_uid: session.uid},
      })
    },

    asterisk_base_reload_access_bans: function() {        
      this._rpc({
        model: 'asterisk_base.access_ban',
        method: 'reload_bans'
      })
    },
  
  });

  var AstBaseFormController = FormController.include({
    
    renderButtons: function($node) {
        this._super.apply(this, arguments)
        if (this.$buttons) {
          let apply_btn = this.$buttons.find('.o_apply_changes');
          apply_btn && apply_btn.click(this.proxy('asterisk_base_apply_changes'));
        }
    },

    asterisk_base_apply_changes: function () {
      this._rpc({
        model: 'asterisk_base.server',
        method: 'apply_all_changes',
        kwargs: {notify_uid: session.uid},
      })
    },
  
  });

});



