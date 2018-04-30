package io.github.legendaries.ass3

import android.content.Intent
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        findViewById<EditText>(R.id.ip_text).setText("104.145.124.182")
        findViewById<EditText>(R.id.port_text).setText("6969")

        findViewById<Button>(R.id.connect_button).setOnClickListener {
            startActivity(
                    Intent(this, TalkActivity::class.java).apply {
                        putExtra("ip", findViewById<EditText>(R.id.ip_text).text.toString())
                        putExtra("port", findViewById<EditText>(R.id.port_text).text.toString())
                    }
            )
        }
    }
}