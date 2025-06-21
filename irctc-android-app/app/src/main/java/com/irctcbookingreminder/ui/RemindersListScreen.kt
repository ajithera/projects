package com.irctcbookingreminder.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.irctcbookingreminder.model.Reminder
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun RemindersListScreen(reminders: List<Reminder>, onBack: () -> Unit, onDelete: (Reminder) -> Unit) {
    val dateFormat = remember { SimpleDateFormat("dd MMM yyyy", Locale.getDefault()) }
    Column(modifier = Modifier.padding(24.dp)) {
        Text("Your Reminders", style = MaterialTheme.typography.headlineSmall)
        Spacer(modifier = Modifier.height(16.dp))
        if (reminders.isEmpty()) {
            Text("No reminders set.", style = MaterialTheme.typography.bodyMedium)
        } else {
            LazyColumn(modifier = Modifier.weight(1f)) {
                items(reminders) { reminder ->
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                    ) {
                        Row(
                            modifier = Modifier.padding(16.dp),
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Column {
                                Text(
                                    "Journey: ${dateFormat.format(Date(reminder.journeyDate))}",
                                    style = MaterialTheme.typography.bodyLarge
                                )
                                Text(
                                    "Reminder: ${dateFormat.format(Date(reminder.reminderDate))}",
                                    style = MaterialTheme.typography.bodySmall
                                )
                                if (reminder.isWeekly) {
                                    Text(
                                        "Weekly: ${reminder.dayOfWeek?.let { dayOfWeekToString(it) } ?: ""}",
                                        style = MaterialTheme.typography.bodySmall
                                    )
                                }
                            }
                            IconButton(onClick = { onDelete(reminder) }) {
                                Icon(Icons.Default.Delete, contentDescription = "Delete")
                            }
                        }
                    }
                }
            }
        }
        Spacer(modifier = Modifier.height(16.dp))
        OutlinedButton(onClick = onBack, modifier = Modifier.fillMaxWidth()) {
            Text("Back")
        }
    }
}

fun dayOfWeekToString(day: Int): String = when(day) {
    Calendar.FRIDAY -> "Friday"
    Calendar.SUNDAY -> "Sunday"
    else -> ""
}
