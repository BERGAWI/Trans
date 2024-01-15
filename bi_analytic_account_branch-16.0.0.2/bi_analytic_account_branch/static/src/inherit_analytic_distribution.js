odoo.define('bi_analytic_account_branch.analytic_distribution', function (require) {
    "use strict";

    const AnalyticDistribution = require("@analytic/components/analytic_distribution/analytic_distribution");
    const { patch } = require('web.utils');
    const core = require('web.core');
    var session = require('web.session');
    var rpc = require('web.rpc');
    const { shallowEqual }= require ("@web/core/utils/arrays");

    let new_inv_branch_id ;
    let branchID ;

    patch(AnalyticDistribution.AnalyticDistribution.prototype, 'bi_analytic_account_branch.analytic_distribution', {
        async willUpdate(nextProps) {
            const valueChanged = JSON.stringify(this.props.value) !== JSON.stringify(nextProps.value);
            const currentAccount = this.props.account_field && this.props.record.data[this.props.account_field] || false;
            const currentProduct = this.props.product_field && this.props.record.data[this.props.product_field] || false;
            const accountChanged = !shallowEqual(this.lastAccount, currentAccount);
            const productChanged = !shallowEqual(this.lastProduct, currentProduct);
            if (valueChanged || accountChanged || productChanged) {
                if (!this.props.force_applicability) {
                    await this.fetchAllPlans(nextProps);
                }
                this.lastAccount = accountChanged && currentAccount || this.lastAccount;
                this.lastProduct = productChanged && currentProduct || this.lastProduct;
                await this.formatData(nextProps);
            }
            var location = self.location.hash
            var pattern = /#id=([^&]+)/;
            var match = location.match(pattern);
            if (match) {
                var id = match[1];
                 rpc.query({
                    model: 'account.move',
                    method: 'get_current_id_method',
                    args: [,id],
                }).then(function (result) {
                        branchID = result;
                     });

            } else {
                new_inv_branch_id = session.allowed_branch_ids[0]
            }

        },
         analyticAccountDomain(groupId=null) {
            let domain = [['id', 'not in', this.existingAnalyticAccountIDs]];
            if (this.props.record.data.company_id){
                domain.push(
                    '|',
                    ['company_id', '=', this.props.record.data.company_id[0]],
                    ['company_id', '=', false]
                );
            }

            if (groupId) {
                domain.push(['root_plan_id', '=', groupId]);
            }

            var inv_location = self.location.hash
            var inv_pattern = /#id=([^&]+)/;
            var inv_model = 'account.move'
            var inv_id_match = inv_location.match(inv_pattern);
            var inv_model_match = inv_location.match(inv_model);
            if (inv_id_match) {
                 domain.push(
                    ['branch_id', '=',branchID]
                );
            }
            else if (inv_model_match) {
                domain.push(
                    ['branch_id', '=',session.user_context.allowed_branch_ids[0]]
                );
            }else {
                domain.push(
                    ['company_id', '=',session.user_context.allowed_company_ids[0]]
                );

            }
            return domain;
        }

    });
});

