package pl.pwr.edu.parser.writer;

import com.fasterxml.jackson.dataformat.xml.XmlMapper;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import javax.xml.bind.JAXB;
import lombok.Setter;
import pl.pwr.edu.parser.domain.Article;
import pl.pwr.edu.parser.writer.path.PathBySourceResolver;
import pl.pwr.edu.parser.writer.path.PathResolver;

/**
 *
 */
public class XMLWriter implements ArticleWriter {

	@Setter
	private PathResolver pathResolver;

	@Override
	public void write(Article article) throws IOException {
		String relativePath = pathResolver.resolveRelativePath(article);
		String absolutePath = pathResolver.getBasePath() + File.separator + relativePath;
		Files.createDirectories(Paths.get(absolutePath));
		String fileName = pathResolver.resolveFileName(article) + ".xml";
		String pathWithFileName = absolutePath + File.separator + fileName;

		Path absolutePathToFile = Paths.get(pathWithFileName);
		File outputXmlFile = absolutePathToFile.toFile();

		XmlMapper xmlMapper = new XmlMapper();

		xmlMapper.writerWithDefaultPrettyPrinter().writeValue(outputXmlFile, article);
	}

	@Override
	public void setPathResolver(PathResolver strategy) {
		this.pathResolver = strategy;
	}

}
