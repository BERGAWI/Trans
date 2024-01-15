# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.model
    def default_get(self, default_fields):
        res = super(AccountAnalyticAccount, self).default_get(default_fields)
        branch_id = False

        if self._context.get('branch_id'):
            branch_id = self._context.get('branch_id')
        elif self.env.user.branch_id:
            branch_id = self.env.user.branch_id.id
        res.update({
            'branch_id': branch_id
        })
        return res

    branch_id = fields.Many2one('res.branch', string="Branch")

    is_b_id_true = fields.Boolean(string='Is true', related='compute_is_b_id_true', store=True)
    compute_is_b_id_true = fields.Boolean(compute='_compute_is_b_id_true', store=False)

    def _compute_is_b_id_true(self):
        for rec in self:
            if rec.branch_id.id == self.env.user.branch_id.id:
                rec.compute_is_b_id_true = True
            else:
                rec.compute_is_b_id_true = False

    def read(self, fields=None, load='_classic_read'):
        data = self.search([])
        data._compute_is_b_id_true()
        return super(AccountAnalyticAccount, self).read(fields=fields, load=load)





class AccountMove(models.Model):
    _inherit = 'account.move'

    is_b_id_true = fields.Boolean(string='Is true', related='compute_is_b_id_true', store=True)
    compute_is_b_id_true = fields.Boolean(compute='_compute_is_b_id_true', store=False)


    def _compute_is_b_id_true(self):
        for rec in self:
            if rec.branch_id.id == self.env.user.branch_id.id:
                rec.compute_is_b_id_true = True
            else:
                rec.compute_is_b_id_true = False

    def read(self, fields=None, load='_classic_read'):
        data = self.search([])
        data._compute_is_b_id_true()
        return super(AccountMove, self).read(fields=fields, load=load)


    def get_current_id_method(self,id):
        current_id =int(id)
        account_move_id = self.env['account.move'].browse(current_id)
        account_current_branch_id = account_move_id.branch_id.id

        return account_current_branch_id
