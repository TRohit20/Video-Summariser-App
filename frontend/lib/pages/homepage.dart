// ignore_for_file: library_private_types_in_public_api

import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:dropdown_button2/dropdown_button2.dart';
import 'package:flutter/material.dart';
import 'package:frontend/pages/summary_result.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage>
    with SingleTickerProviderStateMixin {
  final TextEditingController _videoIdController = TextEditingController();
  String _summary = '';
  String _videoSource = 'youtube'; // Default video source

  AnimationController? _animationController;
  Animation<double>? _animation;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 1000),
      vsync: this,
    );
    _animation = Tween<double>(begin: 0, end: 1).animate(
      CurvedAnimation(
        parent: _animationController!,
        curve: Curves.easeInOut,
      ),
    );
    _animationController!.forward();
  }

  @override
  void dispose() {
    _animationController!.dispose();
    super.dispose();
  }

  Future<void> _getSummary(String videoId, String videoSource) async {
    const url = 'http://127.0.0.1:5000/api/transcribe';
    final response = await http.post(Uri.parse(url), body: {
      'videoId': videoId,
      'videoSource': videoSource,
    });

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

  void _navigateToSummaryPage() {
    final videoId = _videoIdController.text.trim();
    _getSummary(videoId, _videoSource).then((_) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => SummaryResultPage(summary: _summary),
        ),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Summarizer'),
      ),
      body: AnimatedBuilder(
        animation: _animation!,
        builder: (context, child) {
          return Opacity(
            opacity: _animation!.value,
            child: Transform.scale(
              scale: _animation!.value,
              child: child,
            ),
          );
        },
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Enter Video ID:',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              TextField(
                controller: _videoIdController,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: 'Enter the video ID',
                  labelText: 'Video ID',
                ),
              ),
              const SizedBox(height: 16),
              const Text(
                'Select Video Source:',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12.0),
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey),
                  borderRadius: BorderRadius.circular(4.0),
                ),
                child: DropdownButton2<String>(
                  hint: const Text('Select video source'),
                  isExpanded: true,
                  value: _videoSource,
                  onChanged: (String? newValue) {
                    setState(() {
                      _videoSource = newValue!;
                    });
                  },
                  items: const <String>['youtube', 'vimeo']
                      .map<DropdownMenuItem<String>>((String value) {
                    return DropdownMenuItem<String>(
                      value: value,
                      child: Text(value.toUpperCase()),
                    );
                  }).toList(),
                ),
              ),
              const SizedBox(height: 16),
              Center(
                child: ElevatedButton(
                  onPressed: _navigateToSummaryPage,
                  child: const Text('Get Summary'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
