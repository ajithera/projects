package com.irctcbookingreminder.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import java.util.*

@Composable
fun WeeklyReminderScreen(onBack: () -> Unit, onSave: (List<Int>) -> Unit) {
    var fridayChecked by remember { mutableStateOf(false) }
    var sundayChecked by remember { mutableStateOf(false) }

    Column(modifier = Modifier.padding(24.dp)) {
        Text("Set Weekly Reminders", style = MaterialTheme.typography.headlineSmall)
        Spacer(modifier = Modifier.height(24.dp))
        Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically) {
            Checkbox(checked = fridayChecked, onCheckedChange = { fridayChecked = it })
            Spacer(modifier = Modifier.width(8.dp))
            Text("Friday (to Hometown)")
        }
        Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically) {
            Checkbox(checked = sundayChecked, onCheckedChange = { sundayChecked = it })
            Spacer(modifier = Modifier.width(8.dp))
            Text("Sunday (to Work Location)")
        }
        Spacer(modifier = Modifier.height(24.dp))
        Row {
            Button(
                onClick = {
                    val days = mutableListOf<Int>()
                    if (fridayChecked) days.add(Calendar.FRIDAY)
                    if (sundayChecked) days.add(Calendar.SUNDAY)
                    onSave(days)
                },
                enabled = fridayChecked || sundayChecked
            ) {
                Text("Save Weekly Reminders")
            }
            Spacer(modifier = Modifier.width(16.dp))
            OutlinedButton(onClick = onBack) {
                Text("Cancel")
            }
        }
    }
}
