import { useState, useRef, DragEvent, ChangeEvent } from "react";
import { Upload, X, Image as ImageIcon, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
  onClearFile: () => void;
}

export const FileUpload = ({ onFileSelect, selectedFile, onClearFile }: FileUploadProps) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
  const maxFileSize = 5 * 1024 * 1024; // 5MB

  const validateFile = (file: File): string | null => {
    if (!allowedTypes.includes(file.type)) {
      return 'Please upload a JPG, JPEG, or PNG image file.';
    }
    if (file.size > maxFileSize) {
      return 'File size must be less than 5MB.';
    }
    return null;
  };

  const handleFile = (file: File) => {
    const validationError = validateFile(file);
    if (validationError) {
      setError(validationError);
      return;
    }
    
    setError(null);
    onFileSelect(file);
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFile(files[0]);
    }
  };

  const handleFileInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFile(files[0]);
    }
  };

  const openFileDialog = () => {
    fileInputRef.current?.click();
  };

  if (selectedFile) {
    return (
      <div className="card-nature">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0">
            <div className="w-16 h-16 bg-primary/10 rounded-xl flex items-center justify-center">
              <ImageIcon className="w-8 h-8 text-primary" />
            </div>
          </div>
          
          <div className="flex-1 min-w-0">
            <h3 className="text-h3 text-foreground mb-2">Selected Image</h3>
            <p className="text-small text-muted-foreground truncate mb-2">
              {selectedFile.name}
            </p>
            <p className="text-small text-muted-foreground">
              Size: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
            </p>
          </div>
          
          <Button
            variant="ghost"
            size="sm"
            onClick={onClearFile}
            className="flex-shrink-0 text-muted-foreground hover:text-destructive"
          >
            <X className="w-4 h-4" />
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Upload Zone */}
      <div
        className={`upload-zone p-12 text-center ${isDragOver ? 'drag-over' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={openFileDialog}
      >
        <div className="space-y-6">
          {/* Icon */}
          <div className="mx-auto w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center">
            <Upload className="w-10 h-10 text-primary" />
          </div>
          
          {/* Text */}
          <div>
            <h3 className="text-h3 text-foreground mb-2">
              Upload Plant Image
            </h3>
            <p className="text-body text-muted-foreground mb-4">
              Drag and drop your plant leaf image here, or click to browse
            </p>
            <p className="text-small text-muted-foreground">
              Supports JPG, JPEG, PNG • Max 5MB
            </p>
          </div>
          
          {/* Button */}
          <Button className="btn-outline">
            <Upload className="w-4 h-4 mr-2" />
            Choose File
          </Button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="flex items-center gap-2 p-4 bg-destructive/10 border border-destructive/20 rounded-xl text-destructive">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span className="text-small">{error}</span>
        </div>
      )}

      {/* File Requirements */}
      <div className="text-center">
        <p className="text-small text-muted-foreground">
          For best results, upload clear, well-lit images of plant leaves showing any symptoms
        </p>
      </div>

      {/* Hidden File Input */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/jpeg,image/jpg,image/png"
        onChange={handleFileInputChange}
        className="hidden"
      />
    </div>
  );
};