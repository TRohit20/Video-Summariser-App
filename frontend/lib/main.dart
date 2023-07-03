import 'package:flutter/material.dart';
// ignore: depend_on_referenced_packages
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const YoutubeSummaryApp());
}

class YoutubeSummaryApp extends StatelessWidget {
  const YoutubeSummaryApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Summariser',
      theme: ThemeData(
        primarySwatch: Colors.orange,
      ),
      home: const SummaryPage(),
    );
  }
}

class SummaryPage extends StatefulWidget {
  const SummaryPage({Key? key}) : super(key: key);

  @override
  _SummaryPageState createState() => _SummaryPageState();
}

class _SummaryPageState extends State<SummaryPage>
    with SingleTickerProviderStateMixin {
  final TextEditingController _videoIdController = TextEditingController();
  String _summary = '';

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

  void _navigateToSummaryPage() {
    final videoId = _videoIdController.text.trim();
    _getSummary(videoId).then((_) {
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
        title: const Text('Summariser'),
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
              const Center(
                child: Text(
                  'Enter Video ID:',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
              ),
              TextField(
                controller: _videoIdController,
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

class SummaryResultPage extends StatelessWidget {
  final String summary;

  const SummaryResultPage({required this.summary, Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Summary'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              'Summary of the given video is:',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(
              summary,
              style: const TextStyle(fontSize: 16),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
