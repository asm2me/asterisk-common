from datetime import datetime
import logging
from psycopg2.extensions import TransactionRollbackError
from odoo import fields, models, api, registry, _
import time
try:
    import humanize
    HUMANIZE = True
except ImportError:
    HUMANIZE = False



logger = logging.getLogger(__name__)


class PeerRegistry(models.Model):
    _name = 'asterisk_base_sip.peer_registry'
    _description = 'SIP Peer Registry'

    server = fields.Many2one('asterisk_base.server', required=True)
    domain = fields.Char(index=True)
    domain_port = fields.Char()
    host = fields.Char()
    port = fields.Char()
    refresh = fields.Char()
    registration_time = fields.Char()
    username = fields.Char(index=True)
    status = fields.Char()
    domain_port = fields.Char(string=_('Domain'),
                              compute=lambda self: self._compute_domain_port())

    def _compute_domain_port(self):
        for rec in self:
            if rec.port:
                rec.domain_port = '{}:{}'.format(rec.domain, rec.port)
            else:
                rec.domain_port = rec.domain

    @api.model
    def refresh_registry(self):
        # Find peers with registrations
        for server in self.env['asterisk.server'].search([]):
            registries = server.bus_call({'command': 'sip_show_registry'},
                                         timeout=5, silent=True)

            # Remove old Registry
            def remove_records():
                try:
                    with registry(self._cr.dbname).cursor() as cr:
                        env = api.Environment(cr, self.env.user.id, {})
                        env['asterisk.sip_peer_registry'].search(
                                        [('server', '=', server.id)]).unlink()
                    return True
                except Exception as e:
                    logger.warning(e)
                    return False

            # we try 5 times to update the database
            tries = 0
            while tries < 5:
                if not remove_records():
                    tries += 1
                    time.sleep(0.5)
                else:
                    break
            # Now update
            for reg in registries:
                vals = {
                    'server': server.id,
                    'domain': reg['Domain'],
                    'domain_port': reg['DomainPort'],
                    'host': reg['Host'],
                    'port': reg['Port'],
                    'refresh': reg['Refresh'],
                    'username': reg['Username'],
                    'status': reg['State'],
                }
                if HUMANIZE:
                    to_translate = self.env.context.get('lang', 'en_US')
                    if to_translate != 'en_US':
                        humanize.i18n.activate(to_translate)
                    vals['registration_time'] = humanize.naturaltime(
                        datetime.fromtimestamp(float(reg['RegistrationTime']))
                                        ) if reg['RegistrationTime'] else ''
                else:
                    vals['registration_time'] = reg['RegistrationTime']
                try:
                    self.create(vals)
                    self.env.cr.commit()
                except TransactionRollbackError:
                    logger.info('Skip registry create: %s', str(vals))


    @api.model
    def update_registry(self, values):
        if type(values) == list:
            values = values[0]
        server_id = self.env.user.asterisk_base_server.id
        # Search if we have a record already
        existing = self.search([('username', '=', values['Username']),
                                ('domain', '=', values['Domain']),
                                ('server', '=', server_id)])
        if existing:
            existing.write({
                'status': values['Status']
            })
        else:
            self.create({
                'server': server_id,
                'domain': values['Domain'],
                'username': values['Username'],
                'status': values['Status']
            })
        return True
