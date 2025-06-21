package com.irctcbookingreminder.model

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.*

@Entity(tableName = "reminders")
data class Reminder(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val journeyDate: Long, // Epoch millis
    val reminderDate: Long, // Epoch millis (journeyDate - 60 days)
    val isWeekly: Boolean = false, // true for recurring reminders
    val dayOfWeek: Int? = null // Calendar.FRIDAY or Calendar.SUNDAY for weekly
)
