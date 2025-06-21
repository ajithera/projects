package com.irctcbookingreminder.ui

import android.app.DatePickerDialog
import android.content.Context
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun AddJourneyReminderScreen(onBack: () -> Unit, onSave: (Date) -> Unit) {
    val context = LocalContext.current
    var selectedDate by remember { mutableStateOf<Date?>(null) }
    val dateFormat = remember { SimpleDateFormat("dd MMM yyyy", Locale.getDefault()) }

    Column(modifier = Modifier.padding(24.dp)) {
        Text("Add Journey Reminder", style = MaterialTheme.typography.headlineSmall)
        Spacer(modifier = Modifier.height(24.dp))
        Button(onClick = {
            showDatePicker(context) { date ->
                selectedDate = date
            }
        }) {
            Text(selectedDate?.let { dateFormat.format(it) } ?: "Select Journey Date")
        }
        Spacer(modifier = Modifier.height(24.dp))
        Row {
            Button(onClick = { selectedDate?.let { onSave(it) } }, enabled = selectedDate != null) {
                Text("Save Reminder")
            }
            Spacer(modifier = Modifier.width(16.dp))
            OutlinedButton(onClick = onBack) {
                Text("Cancel")
            }
        }
    }
}

fun showDatePicker(context: Context, onDateSelected: (Date) -> Unit) {
    val calendar = Calendar.getInstance()
    DatePickerDialog(
        context,
        { _, year, month, dayOfMonth ->
            calendar.set(year, month, dayOfMonth)
            onDateSelected(calendar.time)
        },
        calendar.get(Calendar.YEAR),
        calendar.get(Calendar.MONTH),
        calendar.get(Calendar.DAY_OF_MONTH)
    ).show()
}
