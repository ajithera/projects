package com.irctcbookingreminder.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.viewModelScope
import com.irctcbookingreminder.data.AppDatabase
import com.irctcbookingreminder.model.Reminder
import kotlinx.coroutines.launch

class ReminderViewModel(application: Application) : AndroidViewModel(application) {
    private val reminderDao = AppDatabase.getDatabase(application).reminderDao()
    val allReminders: LiveData<List<Reminder>> = reminderDao.getAllReminders()

    fun insert(reminder: Reminder) = viewModelScope.launch {
        reminderDao.insert(reminder)
    }

    fun delete(reminder: Reminder) = viewModelScope.launch {
        reminderDao.delete(reminder)
    }
}
