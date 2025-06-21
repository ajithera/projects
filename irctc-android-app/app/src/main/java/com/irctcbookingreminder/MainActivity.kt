package com.irctcbookingreminder

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.irctcbookingreminder.model.Reminder
import com.irctcbookingreminder.ui.AddJourneyReminderScreen
import com.irctcbookingreminder.ui.RemindersListScreen
import com.irctcbookingreminder.ui.WeeklyReminderScreen
import com.irctcbookingreminder.viewmodel.ReminderViewModel
import java.util.*
import com.irctcbookingreminder.ui.theme.IRCTCBookingReminderTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val viewModel: ReminderViewModel by viewModels()
        setContent {
            IRCTCBookingReminderTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    var screen by remember { mutableStateOf("main") }
                    var reminders by remember { mutableStateOf(listOf<Reminder>()) }
                    viewModel.allReminders.observe(this) { reminders = it }
                    when (screen) {
                        "main" -> MainScreen(
                            onAddJourney = { screen = "add_journey" },
                            onWeekly = { screen = "weekly" },
                            onViewReminders = { screen = "reminders" }
                        )
                        "add_journey" -> AddJourneyReminderScreen(
                            onBack = { screen = "main" },
                            onSave = { date ->
                                val journeyMillis = date.time
                                val reminderMillis = journeyMillis - 60L * 24 * 60 * 60 * 1000 // 60 days before
                                viewModel.insert(Reminder(journeyDate = journeyMillis, reminderDate = reminderMillis))
                                screen = "main"
                            }
                        )
                        "weekly" -> WeeklyReminderScreen(
                            onBack = { screen = "main" },
                            onSave = { days ->
                                val now = Calendar.getInstance()
                                for (day in days) {
                                    // Find next occurrence of the selected day
                                    val next = now.clone() as Calendar
                                    val diff = (day + 7 - now.get(Calendar.DAY_OF_WEEK)) % 7
                                    next.add(Calendar.DAY_OF_YEAR, if (diff == 0) 7 else diff)
                                    val journeyMillis = next.timeInMillis
                                    val reminderMillis = journeyMillis - 60L * 24 * 60 * 60 * 1000
                                    viewModel.insert(Reminder(journeyDate = journeyMillis, reminderDate = reminderMillis, isWeekly = true, dayOfWeek = day))
                                }
                                screen = "main"
                            }
                        )
                        "reminders" -> RemindersListScreen(
                            reminders = reminders,
                            onBack = { screen = "main" },
                            onDelete = { reminder -> viewModel.delete(reminder) }
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun MainScreen(
    onAddJourney: () -> Unit = {},
    onWeekly: () -> Unit = {},
    onViewReminders: () -> Unit = {}
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.SpaceBetween
    ) {
        Column {
            Text(
                "IRCTC Booking Reminder",
                style = MaterialTheme.typography.headlineMedium
            )
            Spacer(modifier = Modifier.height(24.dp))
            Button(
                onClick = onAddJourney,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Add Journey Reminder")
            }
            Spacer(modifier = Modifier.height(12.dp))
            Button(
                onClick = onWeekly,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Set Weekly Reminders (Fri/Sun)")
            }
            Spacer(modifier = Modifier.height(12.dp))
            Button(
                onClick = onViewReminders,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("View Reminders")
            }
        }
        Column(modifier = Modifier.fillMaxWidth(), verticalArrangement = Arrangement.Bottom) {
            Divider(modifier = Modifier.padding(vertical = 8.dp))
            Text(
                "Developed by Ajith",
                style = MaterialTheme.typography.bodyMedium
            )
            Text(
                "Contact: ajithera20@gmail.com",
                style = MaterialTheme.typography.bodySmall
            )
            Text(
                "LinkedIn: mjajithkumar",
                style = MaterialTheme.typography.bodySmall
            )
        }
    }
}
