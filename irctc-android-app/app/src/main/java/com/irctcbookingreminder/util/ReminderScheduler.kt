package com.irctcbookingreminder.util

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import com.irctcbookingreminder.model.Reminder
import com.irctcbookingreminder.receiver.ReminderReceiver

object ReminderScheduler {
    fun scheduleReminder(context: Context, reminder: Reminder) {
        val alarmManager = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
        val intent = Intent(context, ReminderReceiver::class.java).apply {
            putExtra("title", "IRCTC Booking Reminder")
            putExtra("message", "Time to book your train ticket for your journey on ${reminder.journeyDate}!")
        }
        val pendingIntent = PendingIntent.getBroadcast(
            context,
            reminder.id,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        alarmManager.setExactAndAllowWhileIdle(
            AlarmManager.RTC_WAKEUP,
            reminder.reminderDate,
            pendingIntent
        )
    }
}
