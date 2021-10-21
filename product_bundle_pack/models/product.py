
from odoo import api, fields, models, _

class ProductPack(models.Model):
	_name = 'product.pack'
	_description = "Product Pack"

	name = fields.Char(string='Name', required=True)
	custom = fields.Float('Custom')
	shipping = fields.Float('Shipping')
	oh = fields.Float('OH')
	margin = fields.Float('Margin')
	risk = fields.Float('Risk')
	total_discount = fields.Float(compute='_compute_total', string='Total Discount', store=True)
	total_ulp = fields.Float(compute='_compute_total', string='Total Unit List Price')
	total_unp = fields.Float(compute='_compute_total', string='Total Unit Net Price', store=True, readonly=True)
	total_tnp = fields.Float(compute='_compute_total', string='Total Net Price', store=True, readonly=True)
	total_ulc = fields.Float(compute='_compute_total', string='Total Unit landed Cost', store=True, readonly=True)
	total_tlc = fields.Float(compute='_compute_total', string='Total landed Cost', store=True, readonly=True)
	total_ucoh = fields.Float(compute='_compute_total', string='Total U.Cost/OH', store=True, readonly=True)
	total_tcoh = fields.Float(compute='_compute_total', string='Total Cost/OH', store=True, readonly=True)
	total_usp = fields.Float(compute='_compute_total', string='Total Unit Selling Price', store=True)
	total_tsp = fields.Float(compute='_compute_total', string='Total Selling Price', store=True, readonly=True)
	state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string="Status", index=True, tracking=True,
							 default="draft")

	groups_ids = fields.One2many('product.pack.line', 'direct_id')

	@api.depends('groups_ids',
				 'groups_ids.product_qty',
				 'groups_ids.discount',
				 'groups_ids.unit_list_price',
				 'groups_ids.unit_net_price',
				 'groups_ids.total_net_price',
				 'groups_ids.unit_landed_cost',
				 'groups_ids.total_landed_cost',
				 'groups_ids.unit_cost_oh',
				 'groups_ids.total_cost_oh',
				 'groups_ids.unit_selling_price',
				 'groups_ids.total_selling_price')
	def _compute_total(self):
		for rec in self:
			rec.total_discount = sum([(p.discount) for p in rec.groups_ids])
			rec.total_ulp = sum([(p.unit_list_price) for p in rec.groups_ids])
			rec.total_unp = sum([(p.unit_net_price) for p in rec.groups_ids])
			rec.total_tnp = sum([(p.total_net_price) for p in rec.groups_ids])
			rec.total_ulc = sum([(p.unit_landed_cost) for p in rec.groups_ids])
			rec.total_tlc = sum([(p.total_landed_cost) for p in rec.groups_ids])
			rec.total_ucoh = sum([(p.unit_cost_oh) for p in rec.groups_ids])
			rec.total_tcoh = sum([(p.total_cost_oh) for p in rec.groups_ids])
			rec.total_usp = sum([(p.unit_selling_price) for p in rec.groups_ids])
			rec.total_tsp = sum([(p.total_selling_price) for p in rec.groups_ids])

	def action_confirm(self):
		product = self.env['product.template']
		already_exist = self.env['product.template'].search([('name', '=', self.name)])
		if already_exist:
			vals_update =product.write({
				'name': self.name,
				'is_pack': True,
				'total_discount': self.total_discount,
				'total_ulp': self.total_ulp,
				'total_unp': self.total_unp,
				'total_tnp': self.total_tnp,
				'total_ulc': self.total_ulc,
				'total_tlc': self.total_tlc,
				'total_ucoh': self.total_ucoh,
				'total_tcoh': self.total_tcoh,
				'total_usp': self.total_usp,
				'total_tsp': self.total_tsp,
				})
			if vals_update:
				for item in self.groups_ids:
					vals_update_lines = product.group_lines.write({
						'product_id': item.product_id.id,
						'discount': item.discount,
						'unit_list_price': item.unit_list_price,
						'unit_net_price': item.unit_net_price,
						'total_net_price': item.total_net_price,
						'unit_landed_cost': item.unit_landed_cost,
						'total_landed_cost': item.total_landed_cost,
						'unit_cost_oh': item.unit_cost_oh,
						'total_cost_oh': item.total_cost_oh,
						'total_selling_price': item.total_selling_price,
						'unit_selling_price': item.unit_selling_price,
						'qty_uom': item.product_qty,
					})
		else:
			vals_create = product.create({
				'name': self.name,
				'is_pack': True,
				'total_discount': self.total_discount,
				'total_ulp': self.total_ulp,
				'total_unp': self.total_unp,
				'total_tnp': self.total_tnp,
				'total_ulc': self.total_ulc,
				'total_tlc': self.total_tlc,
				'total_ucoh': self.total_ucoh,
				'total_tcoh': self.total_tcoh,
				'total_usp': self.total_usp,
				'total_tsp': self.total_tsp,
				})
			if vals_create:
				for item in self.groups_ids:
					vals_create_lines = vals_create.group_lines.create({
						'product_id': item.product_id.id,
						'discount': item.discount,
						'unit_list_price': item.unit_list_price,
						'unit_net_price': item.unit_net_price,
						'total_net_price': item.total_net_price,
						'unit_landed_cost': item.unit_landed_cost,
						'total_landed_cost': item.total_landed_cost,
						'unit_cost_oh': item.unit_cost_oh,
						'total_cost_oh': item.total_cost_oh,
						'total_selling_price': item.total_selling_price,
						'unit_selling_price': item.unit_selling_price,
						'qty_uom': item.product_qty,
						'bi_product_template': int(vals_create.id)
					})
			self.write({'state': 'confirm'})

	def action_draft(self):
		self.write({'state': 'draft'})


class ProductPackLine(models.Model):
	_name = 'product.pack.line'
	_description = "Product Pack Line"

	direct_id = fields.Many2one('product.pack')
	product_id = fields.Many2one('product.product', string='Product', required=True)
	product_qty = fields.Float(string='Quantity', required=True, defaults=1.0)
	bi_product_template = fields.Many2one('product.template', string='Product pack')
	price = fields.Float(related='product_id.lst_price', string='Product Price')
	uom_id = fields.Many2one(related='product_id.uom_id' , string="Unit of Measure", readonly="1")
	name = fields.Char(related='product_id.name')

	discount = fields.Float(string='Discount')
	unit_list_price = fields.Float(string='Unit List Price')
	unit_net_price = fields.Float(compuet='_compute_values', string='Unit Net Price', store=True, readonly=True)
	total_net_price = fields.Float(compute='_compute_values', string='Total Net Price', store=True, readonly=True)
	unit_landed_cost = fields.Float(compute='_compute_values', string='Unit landed Cost', store=True, readonly=True)
	total_landed_cost = fields.Float(_compute_tlc='_compute_values', string='Total landed Cost', store=True, readonly=True)
	unit_cost_oh = fields.Float(compute='_compute_values', string='U.Cost/OH', store=True, readonly=True)
	total_cost_oh = fields.Float(compute='_compute_values', string='T.Cost/OH', store=True, readonly=True)
	unit_selling_price = fields.Float(compute='_compute_values', string='Unit Selling Price', store=True, readonly=True)
	total_selling_price = fields.Float(compute='_compute_values', string='Total Selling Price', store=True, readonly=True)

	@api.depends('direct_id.custom', 'direct_id.margin',
				 'direct_id.shipping', 'direct_id.oh',
				 'direct_id.risk', 'product_qty',
				 'discount', 'unit_list_price')
	@api.onchange('product_id')
	def _compute_values(self):
		for item in self:
			# compuet unit net price
			ulp = item.unit_list_price
			dis = item.discount / 100.0
			item.unit_net_price = ulp * (1.0 - dis)

			# compuete total net price
			item.total_net_price = item.product_qty * item.unit_net_price

			# compute unit landed cost
			cv = item.direct_id.custom / 100.0
			sv = item.direct_id.shipping / 100.0
			item.unit_landed_cost = item.unit_net_price * (1.0 + cv + sv)

			# compute total landed cost
			item.total_landed_cost = item.product_qty * item.unit_landed_cost

			# compute unit cost overhead
			ohv = item.direct_id.oh / 100.0
			rv = item.direct_id.risk / 100.0
			item.unit_cost_oh = item.unit_landed_cost * (1.0 + ohv + rv)

			# compute total cost overhead
			item.total_cost_oh = item.product_qty * item.unit_cost_oh

			# compute unit selling price
			mv = item.direct_id.margin / 100.0
			item.unit_selling_price = item.unit_cost_oh / (1.0 - mv)

			# compute total selling price
			item.total_selling_price = item.product_qty * item.unit_selling_price

class ProductProduct(models.Model):
	_inherit = 'product.template'

	is_pack = fields.Boolean(string='Is Group')
	total_discount = fields.Float(string='Total Discount', readonly=True)
	total_ulp = fields.Float(string='Total Unit List Price', readonly=True)
	total_unp = fields.Float(string='Total Unit Net Price', readonly=True)
	total_tnp = fields.Float(string='Total Net Price', readonly=True)
	total_ulc = fields.Float(string='Total Unit landed Cost', readonly=True)
	total_tlc = fields.Float(string='Total landed Cost', readonly=True)
	total_ucoh = fields.Float(string='Total U.Cost/OH', readonly=True)
	total_tcoh = fields.Float(string='Total Cost/OH', readonly=True)
	total_usp = fields.Float(string='Total Unit Selling Price',)
	total_tsp = fields.Float(string='Total Selling Price', readonly=True)

	group_lines = fields.One2many('product.group.line', 'bi_product_template')


class ProductGroupLines(models.Model):
	_name = 'product.group.line'

	product_id = fields.Many2one('product.product', string='Product', required=True, readonly=True)
	qty_uom = fields.Float(string='Quantity', required=True, defaults=1.0, readonly=True)
	bi_product_template = fields.Many2one('product.template', string='Product pack')
	price = fields.Float(related='product_id.lst_price', string='Product Price')
	uom_id = fields.Many2one(related='product_id.uom_id', string="Unit of Measure", readonly="1")
	name = fields.Char(related='product_id.name', readonly="1")

	discount = fields.Float(string='Discount', readonly=True)
	unit_list_price = fields.Float(string='Unit List Price', readonly=True)
	unit_net_price = fields.Float(string='Unit Net Price', readonly=True)
	total_net_price = fields.Float(string='Total Net Price', readonly=True)
	unit_landed_cost = fields.Float(string='Unit landed Cost', readonly=True)
	total_landed_cost = fields.Float(string='Total landed Cost', readonly=True)
	unit_cost_oh = fields.Float(string='U.Cost/OH', readonly=True)
	total_cost_oh = fields.Float(string='T.Cost/OH', readonly=True)
	unit_selling_price = fields.Float(string='Unit Selling Price', readonly=True)
	total_selling_price = fields.Float(string='Total Selling Price', readonly=True)

