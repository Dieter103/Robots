package io.github.legendaries.ass3

import android.annotation.SuppressLint
import android.app.Activity
import android.os.*
import android.speech.tts.TextToSpeech
import java.util.*

class TTS (val activity: TalkActivity): Thread(), TextToSpeech.OnInitListener {
    lateinit var tts: TextToSpeech
    var init = false

    lateinit var handler: Handler

    override fun onInit(status: Int) {
        if (status != TextToSpeech.SUCCESS) return

        tts.run {
            language = Locale.US
            setPitch(0f)
            setSpeechRate(0f)
        }
    }

    override fun run() {
        if (!init) {
            init = true
            tts = TextToSpeech(activity, this)
        }

        Looper.prepare()

        handler = @SuppressLint("HandlerLeak")
        object: Handler() {
            override fun handleMessage(msg: Message?) {
                super.handleMessage(msg)

                msg?.data?.getString("TT")?.let { speak(it) }
            }
        }

        Looper.loop()
    }

    fun speak(text: String) {
        when {
            Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP -> tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, null)
            else -> tts.speak(text, TextToSpeech.QUEUE_FLUSH, null)
        }

        while (tts.isSpeaking) {
            try {
                Thread.sleep(200)
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }

        activity.connection.handler.run {
            sendMessage(
                    obtainMessage().apply {
                        this.data = Bundle().apply {
                            putString("TT", "done")
                        }
                    }
            )
        }
    }
}