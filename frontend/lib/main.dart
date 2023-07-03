import 'package:flutter/material.dart';
// ignore: depend_on_referenced_packages
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const YoutubeSummaryApp());
}

class YoutubeSummaryApp extends StatelessWidget {
  const YoutubeSummaryApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Youtube Summary App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const SummaryPage(),
    );
  }
}

class SummaryPage extends StatefulWidget {
  const SummaryPage({super.key});

  @override
  _SummaryPageState createState() => _SummaryPageState();
}

class _SummaryPageState extends State<SummaryPage> {
  final TextEditingController _videoIdController = TextEditingController();
  String _summary = '';

  Future<void> _getSummary(String videoId) async {
    const url = 'http://127.0.0.1:5000/api/transcribe';
    final response =
        await http.post(Uri.parse(url), body: {'videoId': videoId});

    if (response.statusCode == 200) {
      final responseData = jsonDecode(response.body);
      setState(() {
        _summary = responseData['summary'];
      });
    } else {
      setState(() {
        _summary = 'Failed to get summary. Please try again.';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Video Summary'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Enter Video ID:',
              style: TextStyle(fontSize: 18),
            ),
            TextField(
              controller: _videoIdController,
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () {
                final videoId = _videoIdController.text.trim();
                _getSummary(videoId);
              },
              child: const Text('Get Summary'),
            ),
            const SizedBox(height: 16),
            const Text(
              'Summary of the given video:',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Expanded(
              child: SingleChildScrollView(
                child: Text(
                  _summary,
                  style: const TextStyle(fontSize: 16),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
