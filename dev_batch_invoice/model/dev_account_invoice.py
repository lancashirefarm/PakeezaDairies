    # -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd. (<http://devintellecs.com>).
#
##############################################################################
from odoo import fields, models, api
from odoo import SUPERUSER_ID
from odoo import netsvc
from datetime import datetime, timedelta

TYPE2JOURNAL = {
    'out_invoice': 'sale',
    'in_invoice': 'purchase',
    'out_refund': 'sale_refund',
    'in_refund': 'purchase_refund',
}


class dev_aco_invoice(models.Model):
    _name='dev.account.invoice'
    _description = "Invoice1"

    @api.model
    def _get_company_default(self):
        company_env = self.env['res.company']
        default_company_id = company_env._company_default_get(
            'dev.account.invoice')
        return company_env.browse(default_company_id.id)

    @api.model
    def _default_journal(self):
        if self._context.get('default_journal_id', False):
            return self.env['account.journal'].browse(self._context.get('default_journal_id'))
        inv_type = self._context.get('type', 'out_invoice')
        inv_types = inv_type if isinstance(inv_type, list) else [inv_type]
        company_id = self._context.get('company_id', self.env.user.company_id.id)
        domain = [
            ('type', 'in', [TYPE2JOURNAL[ty] for ty in inv_types if ty in TYPE2JOURNAL]),
            ('company_id', '=', company_id),
        ]
        return self.env['account.journal'].search(domain, limit=1)

    name = fields.Char(string = 'Sequence',readonly=True, default="MASS INV/",required=True)

#    _defaults = {
#                'name':lambda obj, cr, uid, context: 'MASS INV/',
#                }



    invoice_type = fields.Selection([('cust_invoice','Customer Invoice'),('sup_invoice','Supplier Invoice')],string="Invoice Type", default='cust_invoice' )
#    company_id = fields.Many2one('res.company', string='Company')
    company_id = fields.Many2one('res.company', string='Company', default=_get_company_default)
    journal_id = fields.Many2one('account.journal', string='Journal',default=_default_journal,required=True)

    invoice_ids = fields.One2many('dev.invoice.line','invoice_id', string="Invoice" )
    sup_invoice_ids = fields.One2many('dev.supply.invoice.line','supp_invoice_id', string="Invoice1" )

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),('invoice', 'Invoiced')], string='State', default='draft')
    account_invoice_ids=fields.Many2many('account.invoice',string="Invoices")


#    def create(self, cr, uid, vals, context=None):
#        if vals.get('sequence','/') == '/':
#            vals['name']=self.pool.get('ir.sequence').get(cr,uid,'dev.account.invoice') or '/'
#        res=super(account_invoice, self).create(cr, uid, vals, context=context)
#        return res

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'dev.account.invoice') or 'MASS INV/'
        result = super(dev_aco_invoice, self).create(vals)
        return result


    @api.multi
    def action_invoice(self):
        invoice=[]
        if self.invoice_type == 'cust_invoice':
            for invoice_id in self.invoice_ids:
                res={
                    'partner_id':invoice_id.partner_id.id,
                    'description':invoice_id.description,
                    'date_invoice':invoice_id.date,
                    'account_id':invoice_id.account_id.id,
                    }
                account_obj =  self.env['account.invoice'].create(res)
                invoice.append(account_obj.id)
                if account_obj.id:
                    res={
                    'uom_id':invoice_id.uom_id.id,
                    'account_id':invoice_id.account_id.id,
                    'name':invoice_id.description,
                    'price_unit':invoice_id.amount,
                    'invoice_id':account_obj.id,
                    }
                account_line =  self.env['account.invoice.line'].create(res)

        if self.invoice_type == 'sup_invoice':
            for sup_invoice_id in self.sup_invoice_ids:
                res={
                    'partner_id':sup_invoice_id.partner_id.id,
                    'supplier_invoice_number': sup_invoice_id.supp_invoice_no,
                    'description':sup_invoice_id.description,
                    'date_invoice':sup_invoice_id.date,
                    'account_id':sup_invoice_id.account_id.id,
                    'type': 'in_invoice',
                    }
                account_obj =  self.env['account.invoice'].create(res)
                invoice.append(account_obj.id)
                if account_obj.id:
                    res={
                    'uom_id':sup_invoice_id.uom_id.id,
                    'account_id':sup_invoice_id.account_id.id,
                    'name':sup_invoice_id.description,
                    'price_unit':sup_invoice_id.amount,
                    'invoice_id':account_obj.id,
                    }
                account_line =  self.env['account.invoice.line'].create(res)
        self.account_invoice_ids=[(6, 0, invoice)]
        self.write({'state': 'invoice'})
        return True

    @api.multi
    def action_confirm(self):
        self.write({'state': 'confirm'})
        return True

    @api.multi
    def action_view_invoice(self):
        invoice_ids = self.mapped('account_invoice_ids')
        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('account.action_invoice_tree')
        list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
        form_view_id = imd.xmlid_to_res_id('account.invoice_form')

        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [[list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
        }
        if len(invoice_ids) > 1:
            result['domain'] = "[('id','in',%s)]" % invoice_ids.ids
        elif len(invoice_ids) == 1:
            result['views'] = [(form_view_id, 'form')]
            result['res_id'] = invoice_ids.ids[0]
        else:
            result = {'type': 'ir.actions.act_window_close'}
        return result

class dev_account_invoice(models.Model):
    _name='dev.invoice.line'
    _description = "Invoice2"

    invoice_id = fields.Many2one('dev.account.invoice', string="Invoice" )
    partner_id = fields.Many2one('res.partner',string="Partner", required=True)
    description = fields.Char(string="Description", required=True)
    date = fields.Date(string="Date", required=True)
    uom_id = fields.Many2one('uom.uom',string="UOM", required=True)
    account_id = fields.Many2one('account.account',string="Account", required=True)
    amount = fields.Float(string="Amount", required=True)



class dev_account_invoice(models.Model):
    _name='dev.supply.invoice.line'
    _description = "Invoice3"

    supp_invoice_id = fields.Many2one('dev.account.invoice', string="Invoice" )

    supp_invoice_no = fields.Char(string="Supplier Invoice Number")
    partner_id = fields.Many2one('res.partner',string="Partner", required=True)
    description = fields.Char(string="Description", required=True)
    date = fields.Date(string="Date", required=True)
    uom_id = fields.Many2one('uom.uom',string="UOM", required=True)
    account_id = fields.Many2one('account.account',string="Account", required=True)
    amount = fields.Float(string="Amount", required=True)
