odoo.define('personal.status.type.selection', function (require) {
"use strict";

    var core = require('web.core');
    var relational_fields = require('web.relational_fields');
    var _t = core._t;
    var registry = require('web.field_registry');


    var FieldSelection = relational_fields.FieldSelection;

    var qweb = core.qweb;

    var HierarchySelection = FieldSelection.extend({
        _renderEdit: function () {
            var self = this;
            var prom = Promise.resolve()
            if (!self.hierarchy_groups) {
                prom = this._rpc({
                    model: 'personal.status.type',
                    method: 'search_read',
                    kwargs: {
                        domain: [],
                        fields: ['id', 'display_name', 'type'],
                    },
                }).then(function(arg) {
                    self.values = _.map(arg, v => [v['id'], v['display_name']])
                    self.hierarchy_groups = [
                        {
                            'name': _t('أحوال شخصية'),
                            'children': [
                                {'name': _t('التصنيف العام'), 'ids': _.map(_.filter(arg, v => v['type'] == '1'), v => v['id'])},
                                {'name': _t('دعاوى الأوقاف والوصايا'), 'ids': _.map(_.filter(arg, v => v['type'] == '2'), v => v['id'])},
                                {'name': _t('دعاوى الحضانة والزيارة والنفقة'), 'ids': _.map(_.filter(arg, v => v['type'] == '3'), v => v['id'])},
                                {'name': _t('دعوى النكاح والفرقة'), 'ids': _.map(_.filter(arg, v => v['type'] == '4'), v => v['id'])},
                                {'name': _t('دعاوى الولاية'), 'ids': _.map(_.filter(arg, v => v['type'] == '5'), v => v['id'])},
                                {'name': _t('دعاوى قسمة التركات'), 'ids': _.map(_.filter(arg, v => v['type'] == '6'), v => v['id'])},
                            ],
                        },
                    ]
                });
            }

            Promise.resolve(prom).then(function() {
                self.$el.empty();
                self._addHierarchy(self.$el, self.hierarchy_groups, 0);
                var value = self.value;
                if (self.field.type === 'many2one' && value) {
                    value = value.data.id;
                }
                self.$el.val(JSON.stringify(value));
            });
        },
        _addHierarchy: function(el, group, level) {
            var self = this;
            _.each(group, function(item) {
                var optgroup = $('<optgroup/>').attr(({
                    'label': $('<div/>').html('&nbsp;'.repeat(6 * level) + item['name']).text(),
                }))
                _.each(item['ids'], function(id) {
                    var value = _.find(self.values, v => v[0] == id)
                    optgroup.append($('<option/>', {
                        value: JSON.stringify(value[0]),
                        text: value[1],
                    }));
                })
                el.append(optgroup)
                if (item['children']) {
                    self._addHierarchy(el, item['children'], level + 1);
                }
            })
        }
    });
    registry.add("personal_status_type_selection", HierarchySelection);
});
