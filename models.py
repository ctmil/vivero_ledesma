from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime

class Planta(models.Model):
    _name = 'vivero.planta'

    @api.depends('pedido_ids.qty')
    def _compute_total_ordered(self):
        for rec in self:
            total_ordered = 0
            for pedido in rec.pedido_ids:
                total_ordered = total_ordered + pedido.amount_total
            rec.total_ordered = total_ordered

    def unlink(self):
        if self.pedido_ids:
            raise ValidationError('No se puede borrar una planta con pedidos')
        return super(Planta, self).unlink()

    name = fields.Char("Planta")
    price = fields.Float("Precio")
    pedido_ids = fields.One2many(comodel_name='vivero.pedido',inverse_name='plant_id',string='Plantas')
    total_ordered = fields.Float('Total pedido',compute=_compute_total_ordered,store=True)
    imagen = fields.Binary('Imagen')

class Pedido(models.Model):
    _name = 'vivero.pedido'

    @api.constrains('qty')
    def check_qty(self):
        if self.qty <= 0:
            raise ValidationError('Debe ingresar una cantidad')

    @api.depends('qty')
    def _compute_amount_total(self):
        for rec in self:
            if rec.plant_id.price > 0:
                rec.amount_total = rec.plant_id.price * rec.qty
            else:
                rec.amount_total = 0

    def write(self, vals):
        vals['last_updated'] = str(datetime.now())[:10]
        return super(Pedido, self).write(vals)

    def btn_open(self):
        self.ensure_one()
        sequence = self.env['ir.sequence'].next_by_code('VIVERO')
        self.name = sequence
        self.state = 'open'

    def btn_done(self):
        self.ensure_one()
        self.state = 'done'



    plant_id = fields.Many2one('vivero.planta',string='Planta')
    partner_id = fields.Many2one('res.partner',string='Cliente')
    qty = fields.Integer('Cantidad')
    amount_total = fields.Float('Monto Total',compute=_compute_amount_total,store=True)
    last_updated = fields.Datetime('Ultima actualizacion')
    state = fields.Selection(selection=[('draft','Borrador'),('open','En proceso'),('done','Finalizado')],string="Estado",default="draft")
    name = fields.Char('Pedido')
