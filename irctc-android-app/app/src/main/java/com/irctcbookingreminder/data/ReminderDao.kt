package com.irctcbookingreminder.data

import androidx.lifecycle.LiveData
import androidx.room.*
import com.irctcbookingreminder.model.Reminder

@Dao
interface ReminderDao {
    @Query("SELECT * FROM reminders ORDER BY reminderDate ASC")
    fun getAllReminders(): LiveData<List<Reminder>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(reminder: Reminder)

    @Delete
    suspend fun delete(reminder: Reminder)
}
