from pytz import timezone

from odoo import api, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round, datetime

class Custom_MrpProductProduce(models.TransientModel):
    _inherit = 'mrp.product.produce'

    @api.multi
    def custom_do_produce(self):
        # Nothing to do for lots since values are created using default data (stock.move.lots)
        quantity = self.product_qty
        if float_compare(quantity, 0, precision_rounding=self.product_uom_id.rounding) <= 0:
            raise UserError(
                _("The production order for '%s' has no quantity specified.") % self.product_id.display_name)
        for move in self.production_id.move_finished_ids:
            if move.product_id.tracking == 'none' and move.state not in ('done', 'cancel'):
                rounding = move.product_uom.rounding
                if move.product_id.id == self.production_id.product_id.id:
                    move.quantity_done += float_round(quantity, precision_rounding=rounding)
                elif move.unit_factor:
                    # byproducts handling
                    move.quantity_done += float_round(quantity * move.unit_factor, precision_rounding=rounding)
        self.custom_check_finished_move_lots()
        if self.production_id.state == 'confirmed':
            self.production_id.write({
                'state': 'progress',
                'date_start': datetime.now(),
            })
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def custom_check_finished_move_lots(self):
        produce_move = self.production_id.move_finished_ids.filtered(
            lambda x: x.product_id == self.product_id and x.state not in ('done', 'cancel'))
        if produce_move and produce_move.product_id.tracking != 'none':
            now_utc = datetime.now(timezone('UTC'))
            now_europe = now_utc.astimezone(timezone('Europe/London'))
            lot_name = str(now_europe.strftime("%Y-%m-%d %H:%M:%S"))
            self.lot_id = self.env['stock.production.lot'].create({'name': lot_name,'product_id': self.product_id.id , 'product_qty':self.product_qty,})
            if not self.lot_id:
                raise UserError(_('You need to provide a lot for the finished product.'))
            existing_move_line = produce_move.move_line_ids.filtered(lambda x: x.lot_id == self.lot_id)
            if existing_move_line:
                if self.product_id.tracking == 'serial':
                    raise UserError(_('You cannot produce the same serial number twice.'))
                produced_qty = self.product_uom_id._compute_quantity(self.product_qty,
                                                                     existing_move_line.product_uom_id)
                existing_move_line.product_uom_qty += produced_qty
                existing_move_line.qty_done += produced_qty
            else:
                vals = {
                    'move_id': produce_move.id,
                    'product_id': produce_move.product_id.id,
                    'production_id': self.production_id.id,
                    'product_uom_qty': self.product_qty,
                    'product_uom_id': self.product_uom_id.id,
                    'qty_done': self.product_qty,
                    'lot_id': self.lot_id.id,
                    'location_id': produce_move.location_id.id,
                    'location_dest_id': produce_move.location_dest_id.id,
                }
                self.env['stock.move.line'].create(vals)

        for pl in self.produce_line_ids:
            if pl.qty_done:
                if pl.product_id.tracking != 'none' and not pl.lot_id:
                    raise UserError(_('Please enter a lot or serial number for %s !' % pl.product_id.display_name))
                if not pl.move_id:
                    # Find move_id that would match
                    move_id = self.production_id.move_raw_ids.filtered(
                        lambda m: m.product_id == pl.product_id and m.state not in ('done', 'cancel'))
                    if move_id:
                        pl.move_id = move_id
                    else:
                        # create a move and put it in there
                        order = self.production_id
                        pl.move_id = self.env['stock.move'].create({
                            'name': order.name,
                            'product_id': pl.product_id.id,
                            'product_uom': pl.product_uom_id.id,
                            'location_id': order.location_src_id.id,
                            'location_dest_id': self.product_id.property_stock_production.id,
                            'raw_material_production_id': order.id,
                            'group_id': order.procurement_group_id.id,
                            'origin': order.name,
                            'state': 'confirmed'})
                pl.move_id._generate_consumed_move_line(pl.qty_done, self.lot_id, lot=pl.lot_id)
        return True
