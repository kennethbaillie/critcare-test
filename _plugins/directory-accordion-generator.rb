module Jekyll
  class RenderDirectoryAccordionTag < Liquid::Tag

    def initialize(tag_name, input, tokens)
      super
      @input = input
      puts "Initializing DirectoryAccordion with input: #{@input}" # Log initialization
    end

    def render(context)
      input_split = @input.split('|').map(&:strip)
      directory_path = input_split[0]
      site_source = context.registers[:site].source
      full_path = File.join(site_source, directory_path)

      unless Dir.exists?(full_path)
        puts "DirectoryAccordion Error: The directory '#{full_path}' does not exist." # Log directory not found
        return "Error: The directory does not exist."
      end

      puts "Generating accordion for directory: #{full_path}" # Log directory being processed

      accordion_id = "accordion#{rand(1000)}"

      output = "<div class='accordion' id='#{accordion_id}'>"

      Dir.glob("#{full_path}/**/*").select { |file| File.directory?(file) }.each_with_index do |dir, index|
        dir_name = File.basename(dir)
        item_id = "heading#{index}"
        collapse_id = "collapse#{index}"

        puts "Processing directory: #{dir_name}" # Log directory processing

        output += "<div class='accordion-item'>
                    <h2 class='accordion-header' id='#{item_id}'>
                      <button class='accordion-button collapsed' type='button' data-bs-toggle='collapse' data-bs-target='##{collapse_id}' aria-expanded='true' aria-controls='#{collapse_id}'>
                        #{dir_name}
                      </button>
                    </h2>
                    <div id='#{collapse_id}' class='accordion-collapse collapse' aria-labelledby='#{item_id}' data-bs-parent='##{accordion_id}'>
                      <div class='accordion-body'>"

        Dir.glob("#{dir}/*").each do |file|
          next if File.directory?(file)
          file_name = File.basename(file)
          output += "<a href='#{file.sub(site_source, '')}'>#{file_name}</a><br>"
          puts "Adding file to accordion: #{file_name}" # Log file being added
        end

        output += "   </div>
                    </div>
                  </div>"
      end

      output += "</div>"

      puts "Accordion generated successfully." # Log successful generation

      output
    end
  end
end

Liquid::Template.register_tag('directory_accordion', Jekyll::RenderDirectoryAccordionTag)
