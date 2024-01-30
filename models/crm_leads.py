from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class add_field_for_CRM(models.Model):
    _name = 'crm.lead'
    _inherit = 'crm.lead'
    _description = 'this module update crm form for suitable for laboratory'

    name = fields.Char(string="Sick Name", placeholder="Sick Name", compute="_compute_name")
    image = fields.Image("Status image")
    clinic_id = fields.Many2one('res.partner', string='Clinic Name', domain="[('is_company', '=', True)]")
    doctor_id = fields.Many2one('res.partner', string='Doctor Name', domain="[('parent_id', '=', clinic_id)]")
    doctor_code = fields.Char(string='Doctor Code')
    date_deadline = fields.Date("Delivery Datetime")
    alameensoft_number = fields.Integer("Alameen Soft Number")
    number_of_teeth = fields.Integer("Number of Teeth")
    color_number = fields.Many2one('crm.color', string='Teeth Color')
    lab_team = fields.Selection(selection=[('manager', 'Manager'), ('gypsum', 'Gypsum'), ('cadcam', 'CadCam'), ('porcelain', 'Porcelain'), ('delivery', 'Delivery')], string='Move to')
    datetime_deadline = fields.Datetime(string="Due Datetime")
    team_id = fields.Many2one('crm.team', string="Team")
    flag = fields.Boolean(compute='check_group')
    time = fields.Float(string='Duration in hours ')
    worker_name = fields.Many2many('crm.worker', string='Designer Names')
    porselenci_name = fields.Many2many('crm.porselenci', string='Porselenci Name')
    workers_names = fields.Char(string="Status Workers Names", readonly=True, compute="_calc_workers_names")
    bitim_datetime = fields.Datetime("Bitim", widget='datetime', options={'format': 'YYYY-MM-DD HH:00'})
    dentin_prova = fields.Datetime("Dentin Prova", widget='datetime', options={'format': 'YYYY-MM-DD HH:00'})
    altyapi_prova = fields.Datetime(
        "Altyapi Prova",
        widget='datetime',
        options={'format': 'YYYY-MM-DD HH:00'},
        help="This field is automatically computed but editable",
    )
    teeth_ids = fields.One2many('crm.teeth', 'teeth_id')

    teeth_status = fields.Selection([('Dentin_Prova', 'ZIRKONYUM'),
                                     ('Alt_Yapi', 'GECE PLAĞI'),
                                     ('Abutment_freze', 'IMPLANT ÜSTÜ ZİRKONYUM'),
                                     ('Totalci', 'MUM'),
                                     ('Gecici', 'Gecici'),
                                     ('Metal', 'Metal')], string="Entry status")
    qrcode = fields.Char(string="QR Code", compute="get_qr_code_url", store=True)

    @api.depends('worker_name')
    def _calc_workers_names(self):
        for record in self:
            names = record.worker_name.mapped('name')
            workers_names = ' -> '.join(names)
            record.workers_names = workers_names

    # @api.depends('doctor_id.doctor_code')
    # def _compute_doctor_code(self):
    #     for lead in self:
    #         if lead.doctor_id:
    #             lead.doctor_code = lead.doctor_id.doctor_code
    #         else:
    #             lead.doctor_code = False


    @api.onchange('teeth_ids')
    def _onchange_teeth_ids(self):
        # عند تغيير قيمة teeth_ids، قم بتحديث تاريخ altyapi_prova
        self._compute_date()

    @api.depends('teeth_ids')
    def _compute_date(self):
        for record in self:
            # تحقق من وجود 'ZİRKONYUM' أو 'ABUTMANT_FREZE' في قائمة الأسنان المختارة
            selected_teeth = record.teeth_ids.filtered(lambda teeth: teeth.name in ['ZİRKONYUM',
                                                                                    'ABUTMANT_FREZE',
                                                                                    'IMPLANT_ÜSTÜ_ZİRKONYUM_KRON',
                                                                                    'IMPLANT_ÜSTÜ_POSELEN_KRON',
                                                                                    'TOTALCI',
                                                                                    'METAL_DESTEKLI_PORSELEN_KRON',
                                                                                    'ABUTMANT_FREZE',
                                                                                    'MUM'])

            # إذا كانت المستخدم اختار 'ZİRKONYUM' أو 'ABUTMANT_FREZE'، حدث تاريخ altyapi_prova
            if selected_teeth:
                # احسب التاريخ والوقت ليوم غد في الساعة 17:00
                tomorrow = datetime.now() + timedelta(days=1)
                tomorrow_at_5_pm = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 14, 0)
                record.altyapi_prova = tomorrow_at_5_pm.strftime('%Y-%m-%d %H:%M')

    @api.depends('name')
    def get_qr_code_url(self):
        for record in self:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            qr_code_url = f"{base_url}/web#id={record.id}&cids=1&menu_id=136&action=200&model=crm.lead&view_type=form"
            record.qrcode = qr_code_url

    def back_function(self):
        # قم بتنفيذ الإجراءات التي تريدها هنا
        return {
            'type': 'ir.actions.act_url',
            'url': './web#action=200&model=crm.lead&view_type=kanban&cids=1&menu_id=136',
            'target': 'self',
        }

    def archive_lead(self):
        # قم بتحديث حالة البطاقة إلى مؤرشفة
        self.write({'active': False})
        return {
            'type': 'ir.actions.act_url',
            'url': './web#action=200&model=crm.lead&view_type=kanban&cids=1&menu_id=136',
            'target': 'self',
        }

    def delete_lead(self):
        # حذف البطاقة
        self.unlink()
        return {
            'type': 'ir.actions.act_url',
            'url': './web#action=200&model=crm.lead&view_type=kanban&menu_id=136',
            'target': 'self',
        }

    def open_crm_card(self):
        # قم بتنفيذ السلوك الذي تريده عند الضغط على الزر
        # يمكنك فتح نافذة جديدة هنا أو القيام بأي عمل آخر
        return {
            'name': 'CRM Card',
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'res_id': self.id,
            'view_mode': 'form',
            'view_id': False,
            'target': 'new',
        }


    @api.depends('datetime_deadline')
    def _check_working_hours(self):
        # قم بتحديد ساعات العمل الخاصة بك هنا
        work_start_hour = 9
        work_start_hour = 9
        work_end_hour = 18

        for record in self:
            if record.datetime_deadline:
                deadline_hour = record.datetime_deadline.hour

                # التحقق إذا كانت الساعة ليست في ساعات العمل
                if deadline_hour < work_start_hour or deadline_hour >= work_end_hour:
                    raise ValidationError("Invalid deadline time. Please select a time within working hours.")


    def check_group(self):
        if self.user_has_groups('sales_team.group_sale_salesman'):
            self.flag = True
        else:
            self.flag = False

    # @api.depends('doctor_id')
    # def _compute_name(self):
    #     for lead in self:
    #         if not lead.name and lead.doctor_id and lead.doctor_id.name:
    #             lead.name = ("%s's sick") % lead.doctor_id.name

    @api.depends('doctor_id.email')
    def _compute_email_from(self):
        for lead in self:
            if lead.doctor_id.email:
                lead.email_from = lead.doctor_id.email

    def _inverse_email_from(self):
        for lead in self:
            lead.doctor_id.email = lead.email_from

    @api.depends('doctor_id.phone')
    def _compute_phone(self):
        for lead in self:
            if lead.doctor_id.phone:
                lead.phone = lead.doctor_id.phone

    def _inverse_phone(self):
        for lead in self:
            lead.doctor_id.phone = lead.phone


# class add_field_for_automated(models.Model):
#     _name = 'base.automation'
#     _inherit = 'base.automation'
#     _description = 'this module update crm form for suitable for laboratory'
#
#     activity_date_deadline_range_type = fields.Selection(selection=[('minutes', 'Minutes')])



class color_field_model(models.Model):
    _name = 'crm.color'
    _description = 'this module for teeth color'

    name = fields.Char("Color Number")


class lab_tech_field_model(models.Model):
    _name = 'crm.worker'
    _description = 'this module for lab tech user'

    name = fields.Char("Designer Name")
    product_number = fields.Integer("number")


class lab_porselain_field_model(models.Model):
    _name = 'crm.porselenci'
    _description = 'this module for lab tech user'

    name = fields.Char("Porselenci Name")

class teeth_status(models.Model):
    _name = 'crm.teeth'
    _description = 'this module for lab tech user'

    name = fields.Selection([('ZİRKONYUM', 'ZİRKONYUM'),
                                     ('IMPLANT_ÜSTÜ_ZİRKONYUM_KRON', 'IMPLANT ÜSTÜ ZİRKONYUM KRON'),
                                     ('IMPLANT_ÜSTÜ_POSELEN_KRON', 'IMPLANT ÜSTÜ POSELEN KRON'),
                                     ('METAL_DESTEKLI_PORSELEN_KRON', 'METAL DESTEKLI PORSELEN KRON'),
                                     ('EMAX', 'EMAX + LAMINATE KRON'),
                                     ('GEÇİCİ_KRON', 'GEÇİCİ KRON'),
                                     ('GECE_PLAĞI_SERT', 'GECE PLAĞI SERT'),
                                     ('ABUTMANT_FREZE', 'ABUTMANT FREZE'),
                                     ('MUM', 'MUM'),
                                     ('TOTALCI', 'TOTALCI')], string="Entry status")
    teeth_number = fields.Integer("Teeth Number")
    teeth_id = fields.Many2one('crm.lead')