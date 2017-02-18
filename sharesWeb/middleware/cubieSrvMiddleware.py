# -*- coding: utf-8 -*-
from django.utils.deprecation import MiddlewareMixin
from django.contrib import auth
from django.http import Http404
import globalVars


class CubieSrvMiddleware(MiddlewareMixin):
    # Check if client IP is allowed

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def process_request(self, request):
        allowed_ips = globalVars.djangoIPAuth
        ip = self.get_client_ip(request)
        if ip not in allowed_ips:
            msg = ''
            # msg = 'allowed_ips: ' + allowed_ips +'. '
            msg = msg + 'ATENCION POSIBLE PETICION NO AUTORIZADA DE: ' + ip
            globalVars.toLogFile(msg)
            globalVars.toFile(globalVars.sendFile, msg)
        #    raise Http404  # If user is not allowed raise Error

        try:
            if ip in allowed_ips and not request.user.is_authenticated():
                # Si es una IP de confianza, hacemos el login automatico
                usrName = globalVars.getConfigField('autoLoginUser')
                usrPasswd = globalVars.getConfigField('autoLoginPasswd')
                user = auth.authenticate(username=usrName, password=usrPasswd)
                if user is not None and user.is_active:
                    auth.login(request, user)
                    globalVars.toLogFile('Login automático desde IP: ' + ip)
        except Exception as e:
            globalVars.toLogFile('Error CubieSrvMiddleware.process_request: ' +
                                 str(e))
        return None
