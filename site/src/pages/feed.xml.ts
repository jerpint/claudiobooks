import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export const GET: APIRoute = async ({ site }) => {
  const siteUrl = site?.toString() || 'https://claudiobooks.vercel.app';
  const audiobooks = await getCollection('audiobooks');

  // Sort by date added, newest first
  const sortedAudiobooks = audiobooks.sort(
    (a, b) => b.data.dateAdded.getTime() - a.data.dateAdded.getTime()
  );

  // Build date is used for lastBuildDate
  const lastBuildDate = new Date().toUTCString();

  // Get the most recent episode date for pubDate
  const mostRecentDate = sortedAudiobooks.length > 0
    ? sortedAudiobooks[0].data.dateAdded.toUTCString()
    : lastBuildDate;

  const escapeXml = (str: string): string => {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&apos;');
  };

  const items = sortedAudiobooks.map((audiobook) => {
    const { title, author, description, audioFile, dateAdded, duration } = audiobook.data;
    const audioUrl = `${siteUrl}audio/${audioFile}`;
    const pageUrl = `${siteUrl}audiobook/${audiobook.id}`;

    return `
    <item>
      <title>${escapeXml(title)} by ${escapeXml(author)}</title>
      <link>${pageUrl}</link>
      <description>${escapeXml(description)}</description>
      <pubDate>${dateAdded.toUTCString()}</pubDate>
      <guid isPermaLink="true">${pageUrl}</guid>
      <enclosure url="${audioUrl}" type="audio/mpeg" />
      <itunes:title>${escapeXml(title)}</itunes:title>
      <itunes:author>${escapeXml(author)}</itunes:author>
      <itunes:summary>${escapeXml(description)}</itunes:summary>
      <itunes:duration>${duration}</itunes:duration>
      <itunes:explicit>false</itunes:explicit>
    </item>`;
  }).join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
  xmlns:itunes="http://www.itunes.apple.com/dtds/podcast-1.0.dtd"
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Claudiobooks</title>
    <link>${siteUrl}</link>
    <description>Short-form audiobooks from the public domain, summarized and narrated by AI. Classic literature condensed into 10-20 minute episodes.</description>
    <language>en-us</language>
    <lastBuildDate>${lastBuildDate}</lastBuildDate>
    <pubDate>${mostRecentDate}</pubDate>
    <atom:link href="${siteUrl}feed.xml" rel="self" type="application/rss+xml"/>

    <itunes:author>Claudiobooks</itunes:author>
    <itunes:image href="${siteUrl}podcast-cover.png"/>
    <image>
      <url>${siteUrl}podcast-cover.png</url>
      <title>Claudiobooks</title>
      <link>${siteUrl}</link>
    </image>
    <itunes:summary>Short-form audiobooks from the public domain, summarized and narrated by AI. Classic literature condensed into 10-20 minute episodes.</itunes:summary>
    <itunes:type>episodic</itunes:type>
    <itunes:owner>
      <itunes:name>Claudiobooks</itunes:name>
    </itunes:owner>
    <itunes:explicit>false</itunes:explicit>
    <itunes:category text="Arts">
      <itunes:category text="Books"/>
    </itunes:category>
    <itunes:category text="Education"/>
${items}
  </channel>
</rss>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/rss+xml; charset=utf-8',
    },
  });
};
