from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import ContactForm
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage, message
from django.http import HttpResponse
import textwrap

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mypage/index.html')

class ContactView(View):
    def get(self, request, *args, **kwargs):
        form = ContactForm(request.POST or None)
        return render(request, 'mypage/contact.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST or None)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = 'お問い合わせありがとうございます。'
            contact = textwrap.dedent('''
                ※このメールはシステムからの自動返信です。

                {name}様

                お問い合わせありがとうございました。
                以下の内容でお問い合わせを受け付け致しました。
                内容を確認させて頂き、ご返信させて頂きますので、少々お待ち下さい。
                -----------------
                ■お名前
                {name}様

                ■メールアドレス
                {email}

                ■メッセージ
                {message}
                ''').format(
                    name = name,
                    email = email,
                    message = message
                )
            to_list = [email]
            bcc_list = [settings.EMAIL_HOST_USER]

            try:
                message = EmailMessage(subject=subject, body=contact, to=to_list, bcc=bcc_list)
                message.send()
            except BadHeaderError:
                return HttpResponse('無効なヘッダが検出されました。')

            return redirect('mypage_thanks')

        return render(request, 'mypage/contact.html', {
            'form': form
        })

class ThanksView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mypage/thanks.html')