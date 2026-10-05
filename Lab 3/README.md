# Lab 3 — Chatterboxes: The Listening Lamp

**Xiaoxi Xu**

## Part 1 — Speech Experiments and Initial Design

### A. Text to Speech

**Custom greeting script:** [cici_greeting.sh](speech-scripts/cici_greeting.sh)

#### Voice comparison

For me, eSpeak sounds very robotic, almost like a system announcement in a cyberpunk movie, which makes the greeting feel slightly creepy and distant. In contrast, Piper’s more natural voice makes it feel warmer, more personal, and easier to accept. Even though the words stay exactly the same, the voice changes the perceived distance between me and the speaker, as well as how I feel about who or what is speaking to me.

### B. Speech to Text

#### Model comparison

**Test command:** `python transcribe.py test.wav`

I tested three model sizes with the phrase, “What is the time right now? Is it 12 or 1?” The tiny.en model had a real-time factor of 0.36x, but the transcription was very inaccurate and changed the meaning of the sentence. base.en improved the result with an RTF of 0.75x, correctly recognizing parts like “time right now” and “12,” although it still missed some words. small.en was the most accurate with an RTF of 1.91x, but it took 9.56 seconds to transcribe only 5 seconds of audio and still missed “or 1.”

For a conversational system that needs to respond quickly, I think base.en gives the best tradeoff in this test. The improvement from base.en to small.en was not large enough to justify more than doubling the processing delay. tiny.en was fast, but its errors were significant enough to change the meaning of what I said.

#### Numerical input

**Script:** [ask_time.sh](speech-scripts/ask_time.sh)

I created a script that uses Piper to verbally ask, “What time is it right now?”, records the user's response for five seconds, and then transcribes it using the base.en model.

I noticed that microphone distance had a surprisingly large effect. In my first attempt, I was relatively far from the microphone. My answer was incorrectly transcribed as “All of the way up,” and the transcription took 33.56 seconds with an RTF of 6.71x. When I moved closer to the microphone and tried again, “twelve forty-five” was correctly interpreted as 12.45, and the transcription took only 2.53 seconds with an RTF of 0.51x. This suggests that input quality can affect not only transcription accuracy but also processing time.

### C. Turn-Taking

I tested silence thresholds of 0.2, 0.4, and 1.5 seconds. The default setting of 0.4 seconds felt the most comfortable to me: it allowed brief pauses without making the interaction feel too slow.

At 0.2 seconds, the system sometimes treated a short hesitation as the end of my turn, even though I was still thinking about what to say. Normal speech with pauses around fillers such as “um,” “well,” or “so” could get split into separate segments. For example, “Well” and “So” appeared as standalone transcriptions in my test. This made the interaction feel rushed, as if I had to keep speaking continuously to avoid being cut off.

At 1.5 seconds, I had more room to hesitate and finish my thoughts, but the wait after speaking felt noticeably long. Combined with the additional transcription time, it made the conversation feel very turn-based: I spoke, waited, and then received the result. For me, 0.4 seconds offered the best balance between allowing natural pauses and keeping the interaction responsive.

### D. Storyboard and Design Process

#### Concept

My idea is having someone to talk to after coming home. I chose an Aladdin-inspired lamp because touching it creates a familiar ritual for inviting a companion into a conversation. The lamp acknowledges feelings, asks follow-up questions, and checks whether the user wants listening or advice.

<img width="1774" height="887" alt="idea" src="https://github.com/user-attachments/assets/d7cf50eb-dcf0-4512-8df3-a473375b208b" />

#### Initial user journey

<img width="1536" height="1024" alt="user journey" src="https://github.com/user-attachments/assets/4fdcbd8d-6439-4ba9-8af3-bda04dec6d6a" />

*Concept illustration created with ChatGPT assistance.*

#### Design process and interaction diagram

<img width="984" height="551" alt="截屏2026-10-05 上午5 20 13" src="https://github.com/user-attachments/assets/0b3c6d2e-776f-4f94-a3bd-f307e77b2edc" />

### E. Acting Out the Dialogue

*Reflection not yet added.*

---

## Part 2 — Prototype and Evaluation

### Prototype Storyboard

<img width="1536" height="1024" alt="nex journey" src="https://github.com/user-attachments/assets/7ba4296b-1075-4981-bcba-376423246dd1" />

### Prototype Demonstration

https://github.com/user-attachments/assets/f2098e47-b45a-4f45-816a-c1cedafd666c

### Test Reflections

#### System: What worked and what needs improvement

Overall, the interaction worked, and the back-and-forth conversation communicated the intended experience of a companion that listens and responds. However, participants often needed more time to think while speaking. The system frequently treated these thinking pauses as the end of a turn and cut them off before they had finished. Although the 0.4-second silence threshold felt comfortable in my earlier tests, it was too short in some of these more reflective conversations. I need to adjust the endpointing behavior to give users more room to organize their thoughts.

#### Controller: What worked and what needs improvement

The controller provided a simple way to manage the lamp’s responses. It supported the basic conversation flow, but the manual control made the Wizard of Oz setup too noticeable. A future controller should make these transitions less distracting and better synchronized with the end of the response.

#### Lessons for a More Autonomous System

The tests showed that silence does not necessarily mean someone has finished speaking. In a device designed for sharing feelings, thinking pauses are part of the conversation. A more autonomous version should account for these pauses instead of relying only on a short, fixed silence threshold.

One improvement I would explore is allowing users to touch and hold the lamp while speaking. This would provide an explicit signal: “I am still speaking; please do not interrupt.” While the user maintains contact, the device would keep listening through pauses. Releasing the touch would allow silence detection to resume, rather than immediately ending the turn.

The tests also highlighted the importance of smooth transitions between listening and responding. In a future version, the end of the device’s spoken response should automatically return it to listening, keeping the screen feedback synchronized with the conversation.

#### Interaction Dataset and Additional Sensing

With participants’ consent, I could collect synchronized audio and event logs showing speech activity, detected turn endings, screen states, and researcher button presses. I would annotate moments when participants were still thinking but the system ended their turn, as well as moments when the transition felt appropriate. This could help compare different silence thresholds using actual conversational examples.

For the proposed touch-to-hold interaction, I could also record when users touch and release the lamp, and how long they maintain contact. Comparing touch data with speech and pauses could reveal whether touch provides a useful signal that someone wants to keep their turn.

Video could help show whether participants notice the screen feedback or attempt to continue speaking after being cut off. Short post-test interviews would add their own explanations of these moments.

---

## Course Instructions — Reference Only

<details>
<summary>Original overview, preparation, and setup</summary>

[![Watch the video](https://user-images.githubusercontent.com/1128669/135009222-111fe522-e6ba-46ad-b6dc-d1633d21129c.png)](https://www.youtube.com/embed/Q8FWzLMobx0?start=19)

In this lab, we want you to design interaction with a speech-enabled device — something that listens and talks to you. This device can do anything *but* control lights (since we already did that in Lab 1). First, we want you to storyboard what you imagine the conversational interaction to be like. Then you will use wizarding techniques to elicit examples of what people might say, ask, or respond. We then want you to use the examples collected from at least two other people to inform the redesign of the device.

We will focus on **audio** as the main modality for interaction to start; these general techniques can be extended to **video**, **haptics** or other interactive mechanisms in the second part of the Lab.

A note on what you are building with. Speech interfaces are usually taught as two boxes — speech-in, speech-out — and that framing hides the part that actually determines whether an interaction works. Between listening and speaking sits the question of **whose turn it is**: when does the device decide you have finished talking, and how long does it make you wait before it answers? This lab gives you direct control over both, and we will ask you to notice what changes when you move them.

## Prep for Part 1: Get the Latest Content and Pick up Additional Parts

Please check instructions in [prep.md](prep.md) and complete the setup.

### Pick up Web Camera If You Don't Have One

Students who have not already received a web camera will receive their Webcam and at the beginning of lab. If you cannot make it to class this week, please contact the TAs to ensure you get these.

### Get the Latest Content

As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo.

**\[recommended\]** Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the *personal access token* for this.

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2026
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab3 updates"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your own GitHub repo, create a pull request to get updates from the class Interactive-Lab-Hub. After you have the latest updates online, go to your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull`.

---

# Part 1

## Setup

Create and activate a virtual environment for this lab:

```
pi@ixe00:~$ cd Interactive-Lab-Hub/Lab\ 3
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python3 -m venv .venv
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ source .venv/bin/activate
(.venv) pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $
```

Install the Python dependencies:

```
(.venv) $ pip install -r requirements.txt
```

This takes a few minutes. If you would like it to take considerably less time, [`uv`](https://docs.astral.sh/uv/) is a drop-in replacement for `pip` that is dramatically faster on the Pi:

```
(.venv) $ pip install uv && uv pip install -r requirements.txt
```

Then run the setup script, which installs the classic speech synthesizers, downloads the voice activity detection model, and pre-fetches a neural voice and a speech recognition model so you are not waiting on downloads during lab:

```
(.venv):~$ cd speech-scripts
(.venv) $ ./setup.sh
```

Check your audio devices before going further. `arecord -l` lists capture devices and `aplay -l` lists playback devices; if your webcam microphone or Bluetooth speaker does not appear, fix that first — every script below assumes the system defaults are the ones you want.

</details>

<details>
<summary>Part 1 — Original instructions and example commands</summary>

## A. Text to Speech

Your Pi can speak in several quite different ways, and the differences are audible in a way that matters for design. In `speech-scripts/` there are shell scripts for each.

### The classic engines

```
(.venv) $ cd speech-scripts

(.venv) $ sudo apt update
(.venv) $ sudo apt install -y espeak festival festvox-kallpc16k

(.venv) $ ./espeak_demo.sh
(.venv) $ ./festival_demo.sh
```

You can run these `.sh` files by typing `./filename`, and read one with `cat filename`. You can also play audio files directly with `aplay filename` — try `aplay lookdave.wav`.

These are all decades-old technology and they sound like it. `espeak-ng` is a *formant synthesizer*: it generates speech from an acoustic model of the vocal tract, which is why it sounds robotic but also why the whole thing fits in a couple of megabytes and responds instantly. `festival` is *concatenative*: they stitch together recorded fragments of a real speaker, which sounds more human but breaks audibly at the seams.

### Neural TTS with Piper

Note that the Piper command line changed in version 1.x — voices are now downloaded explicitly with `python3 -m piper.download_voices`, and you invoke it as `python3 -m piper`. Tutorials you find online may show the old `echo ... | piper --model ...` form, which no longer works. Browse the [voice samples](https://rhasspy.github.io/piper-samples) and download a different one if you'd like:

```
(.venv) $ python3 -m piper.download_voices en_US-lessac-medium
```

[Piper](https://github.com/OHF-Voice/piper1-gpl) synthesizes speech with a small neural network, runs comfortably on the Pi 5, and sounds markedly better than the above.

```
(.venv) $ ./piper_demo.sh
```

The demo script also shows `--output-raw`, which streams audio to the speaker as it is generated rather than writing a file first. Listen for the difference in how quickly speech begins. In a conversational system this gap is the thing your user experiences as responsiveness.

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*

\*\***Then answer: Is the same greeting, in these different voices, the same greeting? Describe one concrete way the voice changed what the utterance seemed to mean or who seemed to be speaking.**\*\*

## B. Speech to Text

We use [faster-whisper](https://github.com/SYSTRAN/faster-whisper), a reimplementation of OpenAI's Whisper model that runs several times faster on CPU and does not require PyTorch. All processing happens on the Pi; nothing is sent to a server.

```
(.venv) $ python transcribe.py lookdave.wav
```

The transcript is not the interesting output here — the timings are. Run it again with a larger model and compare:

```
(.venv) $ python transcribe.py lookdave.wav --model base.en
(.venv) $ python transcribe.py lookdave.wav --model small.en
#  noted that the first run may take longer because the model is downloaded, and that the HF unauthenticated-request warning is expected and not an error.
```

Available sizes, smallest first: `tiny.en`, `base.en`, `small.en`, `medium.en`. The `.en` variants are English-only and faster than their multilingual counterparts at the same size.

\*\***Record a few seconds of your own speech (`arecord -d 5 -f cd -c 1 -r 16000 test.wav`) and transcribe it with at least two model sizes. Report the real-time factor for each. At what point does the accuracy improvement stop being worth the delay, for a system that has to answer you?**\*\*

\*\***Write your own script that verbally asks for a numerical input (a phone number, zipcode, number of pets) and records the answer the respondent provides.**\*\*

## C. Turn-taking: knowing when someone has stopped talking

Everything so far has worked on fixed audio files. A real conversational device does not get told when to start and stop recording — it has to decide. This is the problem that makes speech interfaces hard, and it is mostly not a speech recognition problem.

We use a **voice activity detector** (VAD) to segment the microphone stream into utterances. `listen.py` runs Silero VAD continuously and hands each detected utterance to faster-whisper:

```
(.venv) $ cd speech-scripts
(.venv) $ python listen.py
```

Speak, pause, and watch it transcribe. Now change the endpointing threshold — the amount of silence the system requires before it decides your turn is over:

```
(.venv) $ python listen.py --min-silence 0.2
(.venv) $ python listen.py --min-silence 1.5
```

\*\***Try both extremes, and something in between. Describe what each one feels like to talk to. Note specifically: at 0.2s, what kinds of normal speech get cut off? At 1.5s, what does the delay make the system seem like?**\*\*

### The complete loop

`echo_bot.py` puts the pieces together: it listens, endpoints, transcribes, and speaks a reply through Piper. The dialogue policy is deliberately trivial — it repeats what you said — so that everything you notice is a property of the timing rather than the content.

```
(.venv) $ python echo_bot.py
```

## D. Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.)

\*\***Post your storyboard and diagram here.**\*\*

\*\***Please describe and document your process.**\*\*

## E. Acting out the dialogue

Find a partner, and *without sharing the script with your partner* try out the dialogue you've designed, where you (as the device designer) act as the device you are designing. Please record this interaction (for example, using Zoom's record feature).

\*\***Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**\*\*

</details>

<details>
<summary>Part 2 — Original instructions</summary>

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

## Prep for Part 2

1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings.
2. What are other modes of interaction *beyond speech* that you might also use to clarify how to interact? In particular: how does someone know when the device is listening, and when it is thinking? You have a screen and an LED.
3. Make a new storyboard, diagram and/or script based on these reflections.
4. (optional) Integrate [input devices](inputs.md) in the system

## Prototype your system

The system should:
* use the Raspberry Pi
* use one or more sensors
* require participants to speak to it

*Document how the system works.*

*Include videos or screencaptures of both the system and the controller.*

## Test the system

Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard *after* the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?

### What worked well about the controller and what didn't?

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

</details>

<details>
  <summary><strong>Submission Cleanup Reminder (Click to Expand)</strong></summary>

  **Before submitting your README.md:**
  - This readme.md file has a lot of extra text for guidance.
  - Remove all instructional text and example prompts from this file.
  - You may either delete these sections or use the toggle/hide feature in VS Code to collapse them for a cleaner look.
  - Your final submission should be neat, focused on your own work, and easy to read for grading.
</details>
