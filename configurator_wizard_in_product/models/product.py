# -*- coding: utf-8 -*-

from odoo import models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def reconfigure_product(self):
        """ Creates and launches a product configurator wizard with a linked
        template and variant in order to re-configure a existing product. It is
        esetially a shortcut to pre-fill configuration data of a variant"""

        cfg_steps = self.product_tmpl_id.config_step_line_ids
        active_step = str(cfg_steps[0].id) if cfg_steps else 'configure'

        wizard_obj = self.env['product.configurator']
        wizard = wizard_obj.create({
            'product_id': self.id,
            'state': active_step,
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.configurator',
            'name': "Configure Product",
            'view_mode': 'form',
            'context': dict(
                self.env.context,
                wizard_id=wizard.id,
            ),
            'target': 'new',
            'res_id': wizard.id,
        }


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def action_wizard_product_template_configurator(self):
        """ Creates and launches a product configurator wizard with a linked
        template and variant in order to re-configure a existing product. It is
        esetially a shortcut to pre-fill configuration data of a variant"""

        cfg_steps = self.config_step_line_ids
        active_step = str(cfg_steps[0].id) if cfg_steps else 'configure'

        wizard_obj = self.env['product.configurator']
        wizard = wizard_obj.create({
            'product_tmpl_id': self.id,
            'state': active_step,
        })
        ctx_no_type = self._context.copy()
        ctx_no_type.pop('default_type', None)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.configurator',
            'name': "Configure Product",
            'view_mode': 'form',
            'context': dict(
                ctx_no_type,
                wizard_id=wizard.id,
            ),
            'target': 'new',
            'res_id': wizard.id,
        }
