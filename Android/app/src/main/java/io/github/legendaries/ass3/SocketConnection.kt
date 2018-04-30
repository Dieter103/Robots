package io.github.legendaries.ass3

import android.annotation.SuppressLint
import android.os.Handler
import android.os.Looper
import android.os.Message
import android.util.Log
import java.io.PrintWriter
import java.net.Socket
import java.io.BufferedReader
import java.io.InputStreamReader


class SocketConnection(val parent: TalkActivity, val ip: String, val port: Int): Thread() {
    lateinit var socket: Socket
    lateinit var br: BufferedReader

    lateinit var handler: Handler

    var init = false

    override fun run() {
        super.run()

        if (!init) {
            socket = Socket(ip, port)
            br = BufferedReader(InputStreamReader(socket.getInputStream()))
            init = true


            object: Thread() {
                override fun run() {
                    super.run()

                    while (true)
                        readMessage()
                }
            }.start()
        }
        Thread.sleep(2000)

        Looper.prepare()

        // Handle STT send data back to Python
        handler = @SuppressLint("HandlerLeak")
        object: Handler() {
            override fun handleMessage(msg: Message?) {
                super.handleMessage(msg)
                Log.v("Android", "Sending message: $msg over the socket")
                msg?.data?.getString("TT")?.let {
                    writeMessage(it)
                }
            }
        }

        Looper.loop()
    }

    private fun readMessage() {
        var value = ""

        if (!br.ready()) return

        while (br.ready()) {
            value += br.readLine() + "\n"
        }

        if (value.isEmpty()) return

        Log.v("Android", "Received message $value from socket")

        fun parse(str: String) {
            // Server can request tts or sst
            when (str.split(" ")[0]) {
            // Speak the network params if tts
                "tts" -> parent.speakText(str.split(" ").subList(1, str.split(" ").size).joinToString(" "))
            // Send the listened text to the server
                "sst" -> parent.listenForSpeech()
                else -> {}
            }
        }

        if (value.contains("\n")) {
            value.split("\n").forEach {
                parse(it.trim())
            }
        } else {
            parse(value.trim())
        }
    }

    private fun writeMessage(message: String) {
        socket.let {
            try {
                PrintWriter(it.getOutputStream(), true).let {
                    it.run {
                        Log.v("Android", message)
                        print(message)
                        flush()
                    }
                }
            } catch (e: Throwable) {
                e.printStackTrace()
            }
        }
    }
}
