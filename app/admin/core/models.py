from __future__ import annotations

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Section(models.TextChoices):
    MAIN_REPORT = "MAIN_REPORT", _("Кнопки главного меню (отчёт)")   # ← новое
    MARKETBEAT = "MARKETBEAT", _("Ежеквартальный отчет MARKETBEAT")
    SEGMENT = "SEGMENT", _("Обзоры по сегментам рынка")
    ANALYTICS = "ANALYTICS", _("Услуги компании")


class MediaKind(models.TextChoices):
    NONE = "NONE", _("Нет")
    PHOTO = "PHOTO", _("Фото")
    VIDEO = "VIDEO", _("Видео")


class SendStatus(models.TextChoices):
    PENDING = "pending", _("В очереди")
    SENT = "sent", _("Отправлено")
    FAILED = "failed", _("Ошибка")


class Content(models.Model):
    slug = models.SlugField(_("Ключ"), max_length=50, unique=True)
    text = models.TextField(_("Контент"), blank=True)
    media_kind = models.CharField(_("Медиа"), max_length=5, choices=MediaKind.choices, default=MediaKind.NONE)
    media_url = models.URLField(_("URL медиа"), blank=True)
    created_at = models.DateTimeField(_("Создано"), auto_now_add=True)

    class Meta:
        db_table = "contents"
        verbose_name = _("Редактор")
        managed = False
        verbose_name_plural = _("Редактор")

    def __str__(self):
        return self.slug


class MenuButton(models.Model):
    section = models.CharField(_("Раздел"), max_length=15, choices=Section.choices)
    order = models.PositiveIntegerField(_("Порядковый номер"), default=0)
    label = models.CharField(_("Текст кнопки"), max_length=120)
    description = models.TextField(_("Описание"), blank=True)
    media_kind = models.CharField(_("Медиа"), max_length=5, choices=MediaKind.choices, default=MediaKind.NONE)
    media_url = models.URLField(_("URL медиа"), blank=True)
    link_url = models.TextField(
        _("Ссылка или текст сообщения"),
        blank=True,
        help_text=_(
            "Для MARKETBEAT — URL отчёта;"
            "Для Сегментов — ничего;"
            "для консультаций — текст."
        ),
    )

    content = models.ForeignKey(
        Content,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="buttons",
        verbose_name=_("Контент"),
    )

    callback = models.CharField(max_length=64, unique=True, editable=False, default=uuid.uuid4)
    is_active = models.BooleanField(default=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = "menu_buttons"
        verbose_name = _("Кнопка")
        managed = False
        verbose_name_plural = _("Кнопки")
        ordering = ("section", "order")

    def __str__(self):
        return f"[{self.get_section_display()}] {self.label}"


class User(models.Model):
    tg_id = models.BigIntegerField(_("Telegram ID"), unique=True, editable=False)
    full_name = models.CharField(_("ФИО"), max_length=200)
    company = models.CharField(_("Компания"), max_length=200, blank=True)
    position = models.CharField(_("Должность"), max_length=200, blank=True)
    email = models.EmailField(_("E-mail"), blank=True)
    phone = models.CharField(_("Телефон"), max_length=30, blank=True)
    created_at = models.DateTimeField(_("Создан"), auto_now_add=True)

    class Meta:
        db_table = "users"
        verbose_name = _("Пользователь")
        managed = False
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return self.full_name


class ButtonClick(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="clicks",
        verbose_name=_("Пользователь"),
    )
    button = models.ForeignKey(
        MenuButton,
        on_delete=models.CASCADE,
        verbose_name=_("Кнопка"),
    )
    ts = models.DateTimeField(_("Время"), auto_now_add=True)

    class Meta:
        db_table = "button_clicks"
        verbose_name = _("Клик по кнопке")
        verbose_name_plural = _("Клики по кнопкам")
        managed = False
        ordering = ("-ts",)

    def __str__(self):
        return f"{self.user} → {self.button} @ {self.ts:%Y-%m-%d %H:%M:%S}"


class Mailing(models.Model):
    text = models.TextField(_("Сообщение"))
    media_kind = models.CharField(_("Медиа"), max_length=5, choices=MediaKind.choices, default=MediaKind.NONE)
    media_url = models.URLField(_("URL медиа"), blank=True)
    created_at = models.DateTimeField(_("Создана"), auto_now_add=True)

    class Meta:
        db_table = "mailings"
        verbose_name = _("Рассылка")
        verbose_name_plural = _("Рассылки")
        managed = False
        ordering = ("-created_at",)

    def __str__(self):
        return f"Mailing #{self.pk}"


class MailingSend(models.Model):
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name="sends",
        verbose_name=_("Рассылка"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name=_("Получатель"),
    )
    status = models.CharField(
        _("Статус"),
        max_length=7,
        choices=SendStatus.choices,
        default=SendStatus.PENDING,
    )
    ts = models.DateTimeField(_("Время"), auto_now_add=True)

    class Meta:
        db_table = "mailing_sends"
        verbose_name = _("Отправка рассылки")
        verbose_name_plural = _("Отправки рассылок")
        managed = False
        ordering = ("-ts",)

    def __str__(self):
        return f"{self.mailing} → {self.user} [{self.status}]"
